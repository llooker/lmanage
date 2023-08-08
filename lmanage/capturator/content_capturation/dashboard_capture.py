from tqdm import tqdm
import logging
from lmanage.utils import looker_object_constructors as loc, errorhandling as eh, logger_creation as log_color
from yaspin import yaspin

# logger = log_color.init_logger(__name__, logger_level)

logger = log_color.init_logger(__name__, True)


class CaptureDashboards():
    def __init__(self, sdk, content_folders: dict, logger, all_alerts):
        self.sdk = sdk
        self.content_folders = content_folders
        self.logger = logger
        self.all_alerts = all_alerts

    def get_all_dashboards(self) -> dict:
        scrub_dashboards = {}
        with yaspin().white.bold.shark.on_blue as sp:
            sp.text = "getting all system dashboard metadata (can take a while)"
            all_dashboards = self.sdk.all_dashboards(fields="id,folder, slug")

        for dash in all_dashboards:
            logger.info(self.content_folders)
            if dash.folder.id in self.content_folders:
                scrub_dashboards[dash.id] = {}
                scrub_dashboards[dash.id]['folder_id'] = dash.folder.id
                scrub_dashboards[dash.id]['slug'] = dash.slug
        # logger.info(scrub_dashboards)
        return scrub_dashboards

    def get_dashboard_lookml(self, all_dashboards: dict) -> list:
        # logging.info("Beginning Dashboard Capture:")
        response = []
        for dashboard_id in tqdm(all_dashboards, desc="Dashboard Capture", unit="dashboards", colour="#2c8558"):
            lookml = None
            trys = 0
            if "::" in dashboard_id:
                continue
            else:
                dashboard_elements = self.sdk.dashboard(
                    dashboard_id, 'dashboard_elements')['dashboard_elements']
                dashboard_element_ids = [e['id'] for e in dashboard_elements]
                dashboard_element_alert_counts = [
                    e['alert_count'] for e in dashboard_elements]
                scheduled_plans = self.sdk.scheduled_plans_for_dashboard(
                    dashboard_id=dashboard_id, all_users=True)
                alerts = [
                    loc.AlertObject(alert) for alert in self.all_alerts if alert['dashboard_element_id'] in dashboard_element_ids]

                while lookml is None:
                    trys += 1
                    try:
                        lookml = self.sdk.dashboard_lookml(
                            dashboard_id=dashboard_id)
                    except:
                        eh.return_sleep_message(call_number=trys, quiet=True)

                self.logger.debug(lookml.lookml)
                captured_dashboard = loc.DashboardObject(
                    legacy_folder_id=all_dashboards.get(dashboard_id),
                    lookml=lookml.lookml,
                    dashboard_id=dashboard_id,
                    dashboard_slug=all_dashboards.get(
                        dashboard_id).get('slug'),
                    dashboard_element_alert_counts=dashboard_element_alert_counts,
                    scheduled_plans=scheduled_plans,
                    alerts=alerts
                )
                response.append(captured_dashboard)
        return response

    def execute(self):
        all_dashboards = self.get_all_dashboards()
        captured_dash = self.get_dashboard_lookml(all_dashboards)
        return captured_dash
