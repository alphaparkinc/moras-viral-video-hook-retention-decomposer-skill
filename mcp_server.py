import sys, json
from client import ViralVideoHookRetentionDecomposerClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    decomposer = ViralVideoHookRetentionDecomposerClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "moras-viral-video-hook-retention-decomposer-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    segs = req.get("video_segments", [])
    hook_score = req.get("hook_strength_score", 0.85)
    res = decomposer.decompose_video_retention(segs, hook_score)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
