import ReactGA from "react-ga4";

ReactGA.initialize('G-EEL4KXL0BV');

const useAnalyticsEventTracker = (category="test category") => {
  return((action = "test action", label = "test label") => {
    ReactGA.event({
      category,
      action,
      label
    });
  })
}
export default useAnalyticsEventTracker;
