log("loading navigator.languages.js");

utils.replaceProperty(Object.getPrototypeOf(navigator), "languages", {
  get: () => opts.languages,
});
