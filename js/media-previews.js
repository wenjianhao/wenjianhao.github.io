(() => {
  const stills = document.querySelectorAll('picture > source[data-still]');
  const startAnimation = image => {
    // Native lazy loading must not delay a GIF already selected for preloading.
    image.fetchPriority = 'auto';
    image.loading = 'eager';
    const still = image.previousElementSibling;
    if (still?.matches('source[data-still]')) still.remove();
  };
  if ('IntersectionObserver' in window) {
    const near = new IntersectionObserver(entries => {
      for (const {target, isIntersecting} of entries) {
        if (!isIntersecting) continue;
        near.unobserve(target);
        startAnimation(target);
      }
    }, {rootMargin: navigator.connection?.saveData ? '160px 0px' : '600px 0px'});
    stills.forEach(still => near.observe(still.nextElementSibling));
  } else {
    stills.forEach(still => startAnimation(still.nextElementSibling));
  }

  const videos = document.querySelectorAll('video[data-preview]');
  if (!videos.length) return;
  if (!('IntersectionObserver' in window) ||
      matchMedia('(prefers-reduced-motion: reduce)').matches ||
      navigator.connection?.saveData) {
    videos.forEach(video => { video.controls = true; });
    return;
  }
  const observer = new IntersectionObserver(entries => {
    for (const {target, isIntersecting} of entries) {
      if (isIntersecting) target.play().catch(() => { target.controls = true; });
      else target.pause();
    }
  });
  videos.forEach(video => observer.observe(video));
})();
