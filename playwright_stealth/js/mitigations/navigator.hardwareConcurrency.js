log("loading navigator.hardwareConcurrency");

utils.replaceProperty(Object.getPrototypeOf(navigator), "hardwareConcurrency", {
  get() {
    return opts.navigator_hardware_concurrency;
  },
});
