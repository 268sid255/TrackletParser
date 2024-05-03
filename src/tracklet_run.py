from src.utils.tracklet import Tracklet
from src.utils.tracklet_parser import TrackletParser
from typing import List
from src.configs import LABELS_DIR, FRAME_LIST_DIR, OUTPUT_DIR

def main():
    tracklet_labels : str = LABELS_DIR
    frame_list: str = FRAME_LIST_DIR
    output_dir: str = OUTPUT_DIR

    tracklets: List[Tracklet] = TrackletParser.parse_tracklet_xml(tracklet_labels)
    TrackletParser.convert_tracklets_to_kitti(tracklets, frame_list, output_dir)

if __name__ == '__main__':
    main()