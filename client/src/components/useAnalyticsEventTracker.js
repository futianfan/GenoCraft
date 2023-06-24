import ReactGA from "react-ga4";

const useAnalyticsEventTracker = (category="test category") => {
  return((action = "test action", label = "test label") => {
    ReactGA.event({
      category: category,
      action: action,
      label: label
    });
  })
}
export default useAnalyticsEventTracker;
