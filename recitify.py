import cv2
import numpy as np
import argparse
import sys


def main(left_image, right_image, output_image, alpha, debug):

    print("Recitifying images", left_image, "and", right_image, "to", output_image)
    print("Using alpha value of", alpha)

    left = cv2.imread(left_image, cv2.IMREAD_UNCHANGED)
    right = cv2.imread(right_image, cv2.IMREAD_UNCHANGED)

    left_colour = cv2.cvtColor(left, cv2.COLOR_BayerRG2RGB)
    right_colour = cv2.cvtColor(right, cv2.COLOR_BayerRG2RGB)

    if debug:
        cv2.imwrite("L_rgb.png", left_colour)
        cv2.imwrite("R_rgb.png", right_colour)

    cameraMatrix1 = np.array(
        [[1478.4616, 0.0, 940.78233], [0.0, 1474.45028, 679.50984], [0.0, 0.0, 1.0]]
    )
    cameraMatrix2 = np.array(
        [[1478.97446, 0.0, 943.87355], [0.0, 1477.70023, 712.14069], [0.0, 0.0, 1.0]]
    )
    distCoeffs1 = np.array(
        [0.34404, 0.39925000000000005, -0.0024600000000000004, -0.01072, 0.0]
    )
    distCoeffs2 = np.array(
        [0.28774000000000005, 0.6423000000000001, 0.00022, -0.0024200000000000003, 0.0]
    )

    R1 = np.array(
        [
            [0.9999800000000001, -0.0021300000000000004, -0.00517],
            [0.0021100000000000003, 0.99999, -0.00438],
            [0.005180000000000001, 0.004370000000000001, 0.9999800000000001],
        ]
    )

    P1 = np.array(
        [
            [1927.90916, 0.0, 934.55585, 0.0],
            [0.0, 1927.90916, 702.75404, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

    R2 = np.array(
        [
            [0.9998400000000001, 0.009500000000000001, 0.01497],
            [-0.00956, 0.9999500000000001, 0.0043],
            [-0.01493, -0.00444, 0.9998800000000001],
        ]
    )

    P2 = np.array(
        [
            [1927.90916, 0.0, 934.55585, -269.40457],
            [0.0, 1927.90916, 702.75404, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

    if alpha > 0:
        P1, _ = cv2.getOptimalNewCameraMatrix(
            cameraMatrix1, distCoeffs1, (1920, 1440), alpha
        )
        P2, _ = cv2.getOptimalNewCameraMatrix(
            cameraMatrix2, distCoeffs2, (1920, 1440), alpha
        )

    mapLx, mapLy = cv2.initUndistortRectifyMap(
        cameraMatrix1, distCoeffs1, R1, P1, (1920, 1440), cv2.CV_32FC1
    )

    mapRx, mapRy = cv2.initUndistortRectifyMap(
        cameraMatrix2, distCoeffs2, R2, P2, (1920, 1440), cv2.CV_32FC1
    )

    # remap
    left_colour_rect = cv2.remap(left_colour, mapLx, mapLy, cv2.INTER_LANCZOS4)
    right_colour_rect = cv2.remap(right_colour, mapRx, mapRy, cv2.INTER_LANCZOS4)

    # Just for visual aids
    if debug:
        for line in range(0, int(left_colour_rect.shape[0] / 20)):
            if line % 3 == 0:
                left_colour_rect[line * 20, :] = [0, 0, 255]
                right_colour_rect[line * 20, :] = [0, 0, 255]
            elif line % 3 == 1:
                left_colour_rect[line * 20, :] = [0, 255, 255]
                right_colour_rect[line * 20, :] = [0, 255, 255]
            elif line % 3 == 2:
                left_colour_rect[line * 20, :] = [255, 0, 255]
                right_colour_rect[line * 20, :] = [255, 0, 255]

    cv2.imwrite(output_image, np.hstack([left_colour_rect, right_colour_rect]))
    print("Recitification done. Image saved at", output_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recitify of VO images")
    parser.add_argument("--left", type=str, help="Path to left image")
    parser.add_argument("--right", type=str, help="Path to right image")
    parser.add_argument(
        "--output",
        type=str,
        nargs="?",
        default="rectified_pair.png",
        help="Path to output image. Default: rectified_pair.png",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        nargs="?",
        default=0.0,
        help="Alpha value for rectification. Default: 0.0",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Save debug RGB images and show epipolar lines",
    )
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    main(args.left, args.right, args.output, args.alpha, args.debug)
