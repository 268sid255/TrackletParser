from pathlib import Path

#Path
ROOT_DIR = Path(__file__).resolve(strict=True).parent
LABELS_DIR = ROOT_DIR / 'labels' / 'tracklet_labels.xml'
FRAME_LIST_DIR = ROOT_DIR / 'labels' / 'frame_list.txt'
OUTPUT_DIR = ROOT_DIR / 'output'