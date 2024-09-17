log("loading navigator.platform.js");

if (opts.navigator_platform) {
  Object.defineProperty(Object.getPrototypeOf(navigator), "platform", {
    get: () => opts.navigator_platform,
  });
}
