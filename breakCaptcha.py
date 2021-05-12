# Image Processing

import numpy as np
import cv2
from PIL import Image
import zAI
from zAI import zImage

# 이미지 로드
img = cv2.imread('captcha1.png', 0)
#img = cv2.imread('captcha2.png', 0)

# 이미지 대비를 향상
image_enhanced = cv2.equalizeHist(img)

# Adaptive Thresholding 적용
max_output_value = 255   # 출력 픽셀 강도의 최대값
neighborhood_size = 99
subtract_from_mean = 10
image_binarized = cv2.adaptiveThreshold(image_enhanced,
                                       max_output_value,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY,
                                       neighborhood_size,
                                       subtract_from_mean)

# 이미지 not 연산 (흑백 반전)
#horizontal_inv = cv2.bitwise_not(image_binarized)

# and 연산을 수행하여 제공된 마스크로 선을 마스크
masked_img = cv2.bitwise_and(img, img, mask=image_binarized)

# 픽셀 강도의 중간값을 계산
median = np.median(masked_img)

# 중간 픽셀 강도에서 위아래 1 표준편차 떨어진 값을 임곗값으로 지정
lower_threshold = int(max(0, (1.0 - 0.33) * median))
upper_threshold = int(min(255, (1.0 + 0.33) * median))

# Canny edge detection 적용
image_canny = cv2.Canny(masked_img, lower_threshold, upper_threshold)

# image dilation
kernel = np.ones((2,2),np.uint8)
for i in range(1,8):
    dilation = cv2.dilate(image_canny,kernel,iterations = i) # 노이즈 작업 제거 핵심
    cv2.imwrite("img" + str(i) + ".jpg", dilation)



