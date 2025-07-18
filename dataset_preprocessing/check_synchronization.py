import cv2
import os
import numpy as np

def check_video_pair_sync(hr_path, lr_path, output_dir, pair_index):
    """
    Extract and save first, middle, and last frames from a video pair
    """
    # Open both videos
    hr_cap = cv2.VideoCapture(hr_path)
    lr_cap = cv2.VideoCapture(lr_path)
    
    if not hr_cap.isOpened() or not lr_cap.isOpened():
        print(f"Could not open video pair: {hr_path}, {lr_path}")
        return False
    
    # Get video info
    hr_fps = hr_cap.get(cv2.CAP_PROP_FPS)
    lr_fps = lr_cap.get(cv2.CAP_PROP_FPS)
    hr_frames = int(hr_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    lr_frames = int(lr_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Pair {pair_index}: {os.path.basename(hr_path)} / {os.path.basename(lr_path)}")
    print(f"  HR: {hr_frames} frames @ {hr_fps} FPS")
    print(f"  LR: {lr_frames} frames @ {lr_fps} FPS")
    
    # Check frames at beginning, middle, and end
    frames_to_check = [
        (0, "first"),
        (min(hr_frames, lr_frames) // 2, "middle"),
        (min(hr_frames, lr_frames) - 1, "last")
    ]
    
    for frame_idx, position in frames_to_check:
        # Set position in both videos
        hr_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        lr_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        
        # Read frames
        hr_ret, hr_frame = hr_cap.read()
        lr_ret, lr_frame = lr_cap.read()
        
        if not hr_ret or not lr_ret:
            print(f"  Could not read {position} frame (#{frame_idx})")
            continue
        
        # Resize LR frame to match HR frame size
        lr_frame_resized = cv2.resize(lr_frame, (hr_frame.shape[1], hr_frame.shape[0]))
        
        # Place frames side by side
        comparison = np.hstack((hr_frame, lr_frame_resized))
        
        # Add a title
        title = f"Pair {pair_index}, {position} frame (#{frame_idx}): HR (left) vs LR (right)"
        cv2.putText(comparison, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Save the comparison image
        output_path = os.path.join(output_dir, f"pair{pair_index:02d}_{position}_frame{frame_idx:06d}.jpg")
        cv2.imwrite(output_path, comparison)
        print(f"  Saved {position} frame comparison to {output_path}")
    
    hr_cap.release()
    lr_cap.release()
    return True

def check_all_video_pairs(hr_dir, lr_dir, output_dir):
    """
    Check synchronization for all video pairs in the directories
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find video files in directories
    hr_files = sorted([f for f in os.listdir(hr_dir) if f.endswith(('.mov', '.mp4', '.avi'))])
    lr_files = sorted([f for f in os.listdir(lr_dir) if f.endswith(('.mov', '.mp4', '.avi'))])
    
    print(f"Found {len(hr_files)} HR videos and {len(lr_files)} LR videos")
    
    # Find matching pairs (by filename)
    common_files = set(hr_files).intersection(set(lr_files))
    
    if not common_files:
        print("No matching filenames found. Trying to pair by index...")
        # Pair by index if filenames don't match
        video_pairs = [(os.path.join(hr_dir, hr_files[i]), os.path.join(lr_dir, lr_files[i])) 
                      for i in range(min(len(hr_files), len(lr_files)))]
    else:
        print(f"Found {len(common_files)} matching filenames")
        video_pairs = [(os.path.join(hr_dir, f), os.path.join(lr_dir, f)) for f in common_files]
    
    pair_count = 0
    for hr_path, lr_path in video_pairs:
        success = check_video_pair_sync(hr_path, lr_path, output_dir, pair_count)
        if success:
            pair_count += 1
    
    print(f"Processed {pair_count} video pairs")

# Example usage:
output_dir = '/teamspace/studios/this_studio/frame_compare'
check_all_video_pairs('/teamspace/studios/this_studio/original_data/2_0x', 
                     '/teamspace/studios/this_studio/original_data/1_0x',
                     output_dir)