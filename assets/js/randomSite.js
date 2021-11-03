/**
 * This looks for elements with the 'site' class which in this case are all of the
 * anchor links for the sites. This could certainly be made more robust with
 * some sanity checks, but should work in this context.
 */
function randomSite() {
  const sites = document.getElementsByClassName('site')

  if (sites.length > 0) {
    const choiceIndex = Math.floor(Math.random() * sites.length)
    window.open(sites[choiceIndex].attributes.href.value, '_blank').focus()
  }
}
