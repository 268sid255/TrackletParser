from os import makedirs, path
from typing import List, final
from xml.etree.ElementTree import ElementTree
from pandas import read_table
from src.utils.tracklet import Tracklet

@final
class TrackletParser:
    @staticmethod
    def parse_tracklet_xml(tracklet_xml: str) -> List[Tracklet]:
        if not path.exists(tracklet_xml):
            return []
        
        tracklets = TrackletXmlReader.read_tracklets(tracklet_xml)
        TrackletSorter.sort_tracklets(tracklets)
        return tracklets
    
    @staticmethod
    def convert_tracklets_to_kitti(tracklets: List[Tracklet], frame_list: str, output_dir: str):
        if not path.exists(output_dir):
            makedirs(output_dir)
        
        frame_to_file_map = TrackletFrameMapper.get_frame_to_file_map(frame_list)
        TrackletLabelWriter.write_tracklets_to_kitti(tracklets, output_dir, frame_to_file_map)

class TrackletXmlReader:
    @staticmethod
    def read_tracklets(tracklet_xml: str) -> List[Tracklet]:
        tree = ElementTree()
        tree.parse(tracklet_xml)

        tracklets : List[Tracklet] = []
        tracklet_elements = tree.find('tracklets')
        for tracklet_element in tracklet_elements:
            if tracklet_element.tag == 'item':
                tracklet = TrackletBuilder.build_tracklet(tracklet_element)
                tracklets.append(tracklet)
        
        return tracklets

class TrackletBuilder:
    @staticmethod
    def build_tracklet(tracklet_element) -> Tracklet:
        tracklet = Tracklet()
        for attribute in tracklet_element:
            TrackletBuilder._set_tracklet_attribute(tracklet, attribute)
        return tracklet
    
    @staticmethod
    def _set_tracklet_attribute(tracklet: Tracklet, attribute):
        if attribute.tag == 'objectType':
            tracklet.set_type(attribute.text)
        elif attribute.tag == 'h':
            tracklet.set_dimensions('height', float(attribute.text))
        elif attribute.tag == 'w':
            tracklet.set_dimensions('width', float(attribute.text))
        elif attribute.tag == 'l':
            tracklet.set_dimensions('length', float(attribute.text))
        elif attribute.tag == 'first_frame':
            tracklet.set_frame_number(int(attribute.text))
        elif attribute.tag == 'poses':
            TrackletBuilder._set_poses(tracklet, attribute)
    
    @staticmethod
    def _set_poses(tracklet: Tracklet, poses_element):
        for pose in poses_element:
            if pose.tag == 'item':
                TrackletBuilder._set_pose_attributes(tracklet, pose)
    
    @staticmethod
    def _set_pose_attributes(tracklet: Tracklet, pose_element):
        for pose_attribute in pose_element:
            if pose_attribute.tag == 'tx':
                tracklet.set_location('x', float(pose_attribute.text))
            elif pose_attribute.tag == 'ty':
                tracklet.set_location('y', float(pose_attribute.text))
            elif pose_attribute.tag == 'tz':
                tracklet.set_location('z', float(pose_attribute.text))
            elif pose_attribute.tag == 'rz':
                tracklet.set_rotation_z(float(pose_attribute.text))
            elif pose_attribute.tag == 'occulusion':
                tracklet.set_occluded == (int(pose_attribute.text))
            elif pose_attribute.tag == 'truncation':
                tracklet.set_truncated(float(pose_attribute.text))

class TrackletSorter:
    @staticmethod
    def sort_tracklets(tracklets: List[Tracklet]):
        tracklets.sort(key=lambda x: x.frame_number)

class TrackletFrameMapper:
    @staticmethod
    def get_frame_to_file_map(frame_list: str) -> dict:
        if not path.exists(frame_list):
            print('Frame list not found')
            return {}
        
        label_data = read_table(frame_list, delim_whitespace=True, names=['Frame Number', 'File Prefix'], dtype=str,)
        frame_numbers = list(map(int, label_data['Frame Number'].to_list()))
        file_prefixes = list(map(str, label_data['File Prefix'].to_list()))
        return dict(zip(frame_numbers, file_prefixes))

class TrackletLabelWriter:
    @staticmethod
    def write_tracklets_to_kitti(tracklets: List[Tracklet], output_dir: str, frame_to_file_map: dict):
        frames: List[int] = []
        for tracklet in tracklets:
            label = TrackletLabelBuilder.build_label(tracklet)
            label_file_name = TrackletLabelBuilder.get_label_file_name(tracklet.frame_number, frame_to_file_map)
            label_file = path.join(output_dir, f'{label_file_name}.txt')

            if tracklet.frame_number in frames:
                with open(label_file, mode='a', encoding='utf-8') as kitti_file:
                    kitti_file.write(f'{label}\n')
            else:
                with open(label_file, mode='w', encoding='utf-8') as kitti_file:
                    kitti_file.seek(0)
                    kitti_file.write(f'{label}\n')
                    kitti_file.truncate()
                frames.append(tracklet.frame_number)

class TrackletLabelBuilder:
    @staticmethod
    def build_label(tracklet: Tracklet) -> str:
        information = [
            tracklet.type,
            tracklet.truncated,
            tracklet.occluded,
            tracklet.alpha,
            tracklet.bbox["left"],
            tracklet.bbox["top"],
            tracklet.bbox["right"],
            tracklet.bbox["bottom"],
            tracklet.dimensions["height"],
            tracklet.dimensions["width"],
            tracklet.dimensions["length"],
            tracklet.location["x"],
            tracklet.location["y"],
            tracklet.location["z"],
            tracklet.rotation_z,
        ]
        information = list(map(str, information))
        return ' '.join(information)
    
    @staticmethod
    def get_label_file_name(frame_number: int, frame_to_file_map: dict) -> str:
        if frame_number in frame_to_file_map:
            return frame_to_file_map[frame_number]
        else:
            return str(frame_number)