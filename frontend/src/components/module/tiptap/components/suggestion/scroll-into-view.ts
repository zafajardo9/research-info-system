export type ScrollIntoViewDock =
  | "start"
  | "end"
  | "center"
  | "nearest-edge"
  | "nearest";

export interface ScrollIntoViewAxisOptions {
  dock?: ScrollIntoViewDock;
  offset?: number;
  ifNeeded?: boolean;
}

export interface ScrollIntoViewOptions {
  behavior?: ScrollBehavior;
  scrollContainer?: HTMLElement;
  x?: ScrollIntoViewAxisOptions | false;
  y?: ScrollIntoViewAxisOptions | false;
}

type Viewport = HTMLElement | Window;

const isWindow = (element: Viewport): element is Window => {
  return (
    element &&
    !(element as unknown as Record<string, unknown>).getBoundingClientRect
  );
};

const getBCR = (element: Viewport): DOMRect | null => {
  if (isWindow(element)) {
    return null;
  }
  return element.getBoundingClientRect();
};

const getElementOffset = (element: Viewport) => {
  const { top = 0, left = 0 } = getBCR(element) || {};
  const scrollLeft = window.pageXOffset;
  const scrollTop = window.pageYOffset;
  return {
    top: Math.round(top + scrollTop),
    left: Math.round(left + scrollLeft),
  };
};

const getElementDimensons = (element: Viewport, offset?: boolean) => {
  if (isWindow(element)) {
    return {
      width: element.innerWidth,
      height: element.innerHeight,
    };
  }
  if (offset) {
    return {
      width: element.offsetWidth,
      height: element.offsetHeight,
    };
  }
  return {
    width: element.clientWidth,
    height: element.clientHeight,
  };
};

const getElementScroll = (element: Viewport) => {
  if (isWindow(element)) {
    return {
      left: element.scrollX,
      top: element.scrollY,
    };
  }
  return {
    left: element.scrollLeft,
    top: element.scrollTop,
  };
};

const getDockScrollOffset = (
  elementSize: number,
  elementPosition: number,
  viewportSize: number,
  scrollOffset: number,
  dock: ScrollIntoViewDock
) => {
  const base = elementPosition + scrollOffset;
  const start = 0;
  const end = elementSize - viewportSize;
  const center = elementSize / 2 - viewportSize / 2;
  const closestValueReduce = (prev: number, curr: number) =>
    Math.abs(curr + base - scrollOffset) < Math.abs(prev + base - scrollOffset)
      ? curr
      : prev;
  switch (dock) {
    case "start": {
      return start;
    }
    case "end": {
      return end;
    }
    case "center": {
      return center;
    }
    case "nearest-edge": {
      return [start, end].reduce(closestValueReduce);
    }
    case "nearest": {
      return [start, center, end].reduce(closestValueReduce);
    }
  }
};

const defaultDock: ScrollIntoViewDock = "nearest-edge";

export const scrollIntoView = (
  elm?: HTMLElement | null | undefined,
  options?: ScrollIntoViewOptions
) => {
  if (!elm) {
    return;
  }

  const { behavior, scrollContainer, x, y } = options || {};
  const {
    dock: dockX = defaultDock,
    offset: offsetX = 0,
    ifNeeded: ifNeededX = false,
  } = x || {};
  const {
    dock: dockY = defaultDock,
    offset: offsetY = 0,
    ifNeeded: ifNeededY = false,
  } = y || {};
  const doScrollX = x !== false;
  const doScrollY = y !== false;
  const viewport = scrollContainer || window;

  const { left: elementOffsetLeft, top: elementOffsetTop } =
    getElementOffset(elm);
  const { width: elementWidth, height: elementHeight } = getElementDimensons(
    elm,
    true
  );
  const { left: viewportOffsetLeft, top: viewportOffsetTop } =
    getElementOffset(viewport);
  const { width: viewportWidth, height: viewportHeight } =
    getElementDimensons(viewport);
  const { left: viewportScrollLeft, top: viewportScrollTop } =
    getElementScroll(viewport);

  const finalOffsetLeft = elementOffsetLeft - viewportOffsetLeft;
  const finalOffsetTop = elementOffsetTop - viewportOffsetTop;

  const dockOffsetX = getDockScrollOffset(
    elementWidth,
    finalOffsetLeft,
    viewportWidth,
    viewportScrollLeft,
    dockX
  );
  const dockOffsetY = getDockScrollOffset(
    elementHeight,
    finalOffsetTop,
    viewportHeight,
    viewportScrollTop,
    dockY
  );
  const scrollLeft =
    finalOffsetLeft + viewportScrollLeft + dockOffsetX + offsetX;
  const scrolTop = finalOffsetTop + viewportScrollTop + dockOffsetY + offsetY;

  const leftInView =
    elementWidth <= viewportWidth &&
    elementOffsetLeft >= viewportOffsetLeft &&
    elementOffsetLeft + elementWidth <= viewportOffsetLeft + viewportWidth;

  const topInView =
    elementHeight <= viewportHeight &&
    elementOffsetTop >= viewportOffsetTop &&
    elementOffsetTop + elementHeight <= viewportOffsetTop + viewportHeight;

  const scrollXNeeded = doScrollX && (ifNeededX ? !leftInView : true);
  const scrollYNeeded = doScrollY && (ifNeededY ? !topInView : true);

  if (scrollXNeeded || scrollYNeeded) {
    viewport.scrollTo({
      left: doScrollX ? scrollLeft : undefined,
      top: doScrollY ? scrolTop : undefined,
      behavior,
    });
  }
};
