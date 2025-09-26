import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import asyncio
import logging

# Import ContextMonitor and SuggestionEngine
from semantic_self_aware_kit.context_monitoring import ContextMonitor
from semantic_self_aware_kit.intelligent_suggestions import SuggestionEngine

class ProactiveMonitorEventHandler(FileSystemEventHandler):
    """Handles file system events and triggers context updates and suggestions."""
    def __init__(self, context_monitor: ContextMonitor, suggestion_engine: SuggestionEngine):
        super().__init__()
        self.context_monitor = context_monitor
        self.suggestion_engine = suggestion_engine
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO) # Set logging level for this handler

    def on_modified(self, event):
        if not event.is_directory:
            self.logger.info(f"File modified: {event.src_path}")
            self._trigger_proactive_suggestion()

    def on_created(self, event):
        if not event.is_directory:
            self.logger.info(f"File created: {event.src_path}")
            self._trigger_proactive_suggestion()

    def on_deleted(self, event):
        if not event.is_directory:
            self.logger.info(f"File deleted: {event.src_path}")
            self._trigger_proactive_suggestion()

    def on_moved(self, event):
        if not event.is_directory:
            self.logger.info(f"File moved: {event.src_path} to {event.dest_path}")
            self._trigger_proactive_suggestion()

    def _trigger_proactive_suggestion(self):
        """Triggers context update and suggestion generation."""
        self.logger.info("Triggering proactive suggestion...")
        try:
            # Get updated context
            active_context = self.context_monitor.get_active_context(time_window_minutes=1) # Look for very recent changes

            # Generate suggestions
            suggestions = self.suggestion_engine.generate_suggestions(active_context)

            if suggestions:
                self.logger.info("\n--- PROACTIVE SUGGESTIONS ---")
                for s in suggestions:
                    self.logger.info(f"- {s['description']} (Component: {s['component']}, Priority: {s['priority']:.2f})")
                    self.logger.info(f"  Command: `{s['cli_command']}`")
                self.logger.info("-----------------------------\n")
            else:
                self.logger.info("No specific proactive suggestions at this moment.")

        except Exception as e:
            self.logger.error(f"Error during proactive suggestion generation: {e}")


class ProactiveMonitor:
    """Monitors the file system for changes and triggers proactive suggestions."""
    def __init__(self, path: str, root_dir: str = None):
        self.path = Path(path)
        self.observer = Observer()
        self.context_monitor = ContextMonitor(root_dir=root_dir)
        self.suggestion_engine = SuggestionEngine()
        self.event_handler = ProactiveMonitorEventHandler(self.context_monitor, self.suggestion_engine)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO) # Set logging level for this monitor

    def start(self):
        """Starts monitoring the specified path."""
        if not self.path.exists():
            self.logger.error(f"Path to monitor does not exist: {self.path}")
            return

        self.logger.info(f"Starting proactive monitoring of: {self.path}")
        self.observer.schedule(self.event_handler, str(self.path), recursive=True)
        self.observer.start()
        self.logger.info("Proactive monitor started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stops the monitoring."""
        self.logger.info("Stopping proactive monitor...")
        self.observer.stop()
        self.observer.join()
        self.logger.info("Proactive monitor stopped.")

# Example usage (for testing purposes)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Monitor the current working directory
    monitor_path = os.getcwd()
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    proactive_monitor = ProactiveMonitor(monitor_path, root_dir=project_root)
    proactive_monitor.start()
