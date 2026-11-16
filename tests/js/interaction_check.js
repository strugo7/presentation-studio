// Drives a rendered HTML deck in headless Chromium and prints a JSON report.
// usage: node interaction_check.js /abs/path/index.html <quizSlideId> <pollSlideId>
const { chromium } = require('playwright');
(async () => {
  const [idx, quizId, pollId] = process.argv.slice(2);
  const b = await chromium.launch();
  const out = { errors: [] };
  try {
    const pg = await b.newPage({ viewport: { width: 1280, height: 720 } });
    pg.on('pageerror', e => out.errors.push(String(e)));
    await pg.goto('file://' + idx); await pg.waitForTimeout(300);
    const slideIndex = id => pg.evaluate(id => [...document.querySelectorAll('.slide')].findIndex(s => s.id === 's-' + id), id);
    // quiz: Enter on an option must answer, not advance
    const qi = await slideIndex(quizId);
    await pg.evaluate(i => deck.go(i, { inst: true }), qi); await pg.waitForTimeout(100);
    const opts = pg.locator(`#s-${quizId} .opt`);
    await opts.nth(1).focus(); await pg.keyboard.press('Enter');
    out.afterEnterIdx = (await pg.evaluate(() => deck.state())).idx; out.quizIdx = qi;
    out.wrongFeedback = await pg.locator(`#s-${quizId} .eg-fb`).textContent();
    out.wrongClass = await opts.nth(1).getAttribute('class');
    await pg.keyboard.press('ArrowDown');
    out.focusMoved = await pg.evaluate(() => document.activeElement.dataset.opt);
    await pg.keyboard.press(' ');
    out.afterSpaceIdx = (await pg.evaluate(() => deck.state())).idx;
    out.rightChecked = await opts.nth(2).getAttribute('aria-checked');
    await pg.locator(`#s-${quizId} .eg-reveal`).click();
    out.revealFeedback = await pg.locator(`#s-${quizId} .eg-fb`).textContent();
    out.correctMarked = await pg.locator(`#s-${quizId} .opt.ok`).getAttribute('data-opt');
    // poll: local counts
    const pi = await slideIndex(pollId);
    await pg.evaluate(i => deck.go(i, { inst: true }), pi); await pg.waitForTimeout(100);
    const po = pg.locator(`#s-${pollId} .opt`);
    await po.nth(0).click(); await po.nth(0).click(); await po.nth(1).click();
    out.pollCounts = [await po.nth(0).locator('.cnt').textContent(), await po.nth(1).locator('.cnt').textContent()];
    // deck keys still work when focus is outside the interaction
    await pg.evaluate(() => { document.activeElement && document.activeElement.blur(); deck.go(0, { inst: true }); });
    await pg.keyboard.press('ArrowRight'); await pg.waitForTimeout(50);
    out.arrowIdx = (await pg.evaluate(() => deck.state())).idx;
    out.rmDefault = (await pg.evaluate(() => deck.state())).RM;
    // reduced motion from the OS setting
    const pg2 = await b.newPage({ viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce' });
    await pg2.goto('file://' + idx); await pg2.waitForTimeout(300);
    out.rmReduce = await pg2.evaluate(() => deck.state().RM && document.body.classList.contains('rm'));
    // offline: no external requests at all
    const pg3 = await b.newPage(); const ext = [];
    pg3.on('request', r => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:')) ext.push(r.url()); });
    await pg3.goto('file://' + idx); await pg3.waitForTimeout(300);
    out.externalRequests = ext;
  } catch (e) { out.errors.push(String(e)); }
  await b.close();
  console.log(JSON.stringify(out));
})();
