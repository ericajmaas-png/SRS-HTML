// Retained legacy views are tested directly when they no longer have a sidebar shortcut.
// Current product navigation is exercised through real clicks in test_simple_overview.cjs.
module.exports=async function navigate(p,id){let button=p.locator(`#nav [data-page="${id}"]`);if(await button.count()){await button.evaluate(e=>{let d=e.closest('details');if(d)d.open=true});await button.click()}else await p.evaluate(i=>{page=i;render()},id)};
