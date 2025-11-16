"""
Context Compaction configs uses a sliding window approach for collecting and summarizing agent workflow
event data within a Session.
"""

from google.adk.apps.app import EventsCompactionConfig

context_compaction_config: EventsCompactionConfig = EventsCompactionConfig(
    compaction_interval=5,  # Trigger compaction every 5 new invocations.
    overlap_size=1  # Include last invocation from the previous window.
)
