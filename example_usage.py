from client import ViralVideoHookRetentionDecomposerClient
import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    decomposer = ViralVideoHookRetentionDecomposerClient()
    print("=== MORAS VIRAL VIDEO HOOK RETENTION DECOMPOSER ===")

    # Standard 28-second high-converting TikTok Shop short-form script
    script_segments = [
        {"segment_type": "HOOK",              "duration_sec": 3.0, "visual_intensity": 0.95, "speech_wpm": 165},
        {"segment_type": "PROBLEM_AGITATION", "duration_sec": 4.5, "visual_intensity": 0.80, "speech_wpm": 150},
        {"segment_type": "PRODUCT_DEMO",      "duration_sec": 9.0, "visual_intensity": 0.85, "speech_wpm": 155},
        {"segment_type": "SOCIAL_PROOF",      "duration_sec": 6.5, "visual_intensity": 0.70, "speech_wpm": 145},
        {"segment_type": "CTA_OFFER",         "duration_sec": 5.0, "visual_intensity": 0.90, "speech_wpm": 170}
    ]

    res = decomposer.decompose_video_retention(script_segments, hook_strength_score=0.92)
    print()
    print(f"Total Video Runtime : {res['total_duration_sec']}s")
    print(f"3s Hook Retention   : {res['three_second_hook_retention_pct']}%")
    print(f"Final Completion    : {res['final_completion_rate_pct']}%")
    print(f"Performance Verdict : {res['performance_classification']}")
    print()
    print("Segment Progression Timeline:")
    for seg in res['segments_breakdown']:
        print(f"  [{seg['segment_type']:<17}] {seg['duration_sec']:4.1f}s -> Retention: {seg['start_retention_pct']}% to {seg['end_retention_pct']}% (Drop: -{seg['segment_dropoff_pct']}%)")

if __name__ == "__main__":
    main()
