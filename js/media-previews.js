(() => {
  const stills = document.querySelectorAll('picture > source[data-still]');
  if ('IntersectionObserver' in window) {
    const near = new IntersectionObserver(entries => {
      for (const {target, isIntersecting} of entries) {
        if (!isIntersecting) continue;
        near.unobserve(target);
        target.previousElementSibling.remove();
      }
    }, {rootMargin: '160px 0px'});
    stills.forEach(still => near.observe(still.nextElementSibling));
  } else {
    stills.forEach(still => still.remove());
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
