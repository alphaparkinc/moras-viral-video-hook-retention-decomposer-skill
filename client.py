import sys, math
sys.stdout.reconfigure(encoding='utf-8')

class ViralVideoHookRetentionDecomposerClient:
    """
    K2 Prism inspired short-form commerce video retention deconstruction engine.
    Analyzes structural segments: Hook (0-3s), Problem Agitation (3-7s), Product Showcase (7-16s),
    Social Proof (16-23s), and Call to Action (23-30s).
    Models audience hazard decay rate lambda(t) and estimates 3-second hook retention and completion index.
    """
    def __init__(self):
        # Baseline hazard decay factors per narrative segment
        self.segment_baseline_hazards = {
            "HOOK": 0.08,             # Crucial 0-3s filter
            "PROBLEM_AGITATION": 0.04, # 3-7s emotional validation
            "PRODUCT_DEMO": 0.025,     # 7-16s core value prop
            "SOCIAL_PROOF": 0.02,      # 16-23s credibility reinforcement
            "CTA_OFFER": 0.035         # 23-30s closing friction
        }

    def decompose_video_retention(self, video_segments, hook_strength_score=0.85):
        """
        video_segments: list of dicts:
        {"segment_type": str, "duration_sec": float, "visual_intensity": float, "speech_wpm": float}
        """
        if not video_segments:
            return {"status": "error", "message": "No video segments supplied"}

        total_duration = sum(s.get("duration_sec", 0.0) for s in video_segments)
        current_retention = 1.0
        retention_timeline = []
        elapsed_sec = 0.0

        for seg in video_segments:
            stype = seg.get("segment_type", "PRODUCT_DEMO").upper()
            dur = float(seg.get("duration_sec", 5.0))
            intensity = float(seg.get("visual_intensity", 0.7)) # 0.0 - 1.0
            wpm = float(seg.get("speech_wpm", 150.0))

            base_hazard = self.segment_baseline_hazards.get(stype, 0.03)
            
            # Pacing and intensity damping factors
            # High visual intensity and optimal WPM (140-170) lower drop-off hazard
            pacing_penalty = max(0.0, (wpm - 160.0) / 400.0) if wpm > 160 else max(0.0, (140.0 - wpm) / 300.0)
            adjusted_hazard = base_hazard * (1.3 - (intensity * 0.4)) + pacing_penalty
            
            if stype == "HOOK":
                # Hook strength directly mitigates initial drop
                adjusted_hazard *= (1.5 - hook_strength_score)

            segment_survival = math.exp(-adjusted_hazard * dur)
            start_retention = current_retention
            end_retention = current_retention * segment_survival
            current_retention = end_retention

            elapsed_sec += dur
            retention_timeline.append({
                "segment_type": stype,
                "duration_sec": dur,
                "cumulative_timestamp_sec": round(elapsed_sec, 2),
                "start_retention_pct": round(start_retention * 100, 1),
                "end_retention_pct": round(end_retention * 100, 1),
                "segment_dropoff_pct": round((start_retention - end_retention) * 100, 1),
                "effective_hazard_rate": round(adjusted_hazard, 4)
            })

        three_sec_retention = retention_timeline[0]["end_retention_pct"] if retention_timeline else 0.0
        final_completion = current_retention * 100

        grade = "VIRAL_POTENTIAL" if three_sec_retention >= 70.0 and final_completion >= 25.0 else ("ABOVE_AVERAGE" if three_sec_retention >= 55.0 else "HIGH_CHURN_RISK")

        return {
            "status": "success",
            "total_duration_sec": round(total_duration, 1),
            "three_second_hook_retention_pct": round(three_sec_retention, 1),
            "final_completion_rate_pct": round(final_completion, 1),
            "performance_classification": grade,
            "segments_breakdown": retention_timeline
        }
