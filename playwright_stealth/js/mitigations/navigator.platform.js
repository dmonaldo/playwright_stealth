log("loading navigator.platform.js");

if (opts.navigator_platform) {
  utils.replaceProperty(Object.getPrototypeOf(navigator), "platform", {
    get: () => opts.navigator_platform,
  });
}
