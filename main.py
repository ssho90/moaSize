import cv2
import os
import sys
import math
import shutil

def change_img_qualty(original_path, change_path, temp_path):
    """
    Change Image Qualty
    :param original_path: 원본 경로
    :param change_path: 변경 후 새롭게 저장될 경로
    :return:
    """

    InputTargetSize = input(">>>>> 사진 용량을 몇 MB로 줄이고 싶나요? (숫자만 입력) : ")
    print(" ")
    targetSize = math.ceil(float(InputTargetSize) * 1024 * 1024)


    if not os.path.exists(change_path):
        os.mkdir(change_path)
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    try:
        ims_list = os.listdir(original_path)
        ims_list.sort()
    except FileNotFoundError as e:
        print("이미지 원본 디렉터리가 존재하지 않습니다...")
        sys.exit(0)

    success_cnt = 0
    fail_cnt = 0
    file_idx = 0
    failed_file_list = []

    print("*********************** 변환 시작 ***********************")

    for filename in ims_list:
        quality = 80
        originFile = original_path + filename
        originImg = cv2.imread(originFile)
        file_idx += 1
        origin_file_size = os.path.getsize(originFile)

        if (origin_file_size < targetSize):
            #원본이 이미 target size보다 작을때 원본 그대로 카피
            shutil.copy2(originFile, change_path + filename)
            print(str(file_idx) + ". " + filename + " 변경에 성공 했습니다. 변경된 파일 용량 : " + str(round(origin_file_size / 1024 / 1024, 1)) + "MB")
            success_cnt += 1
        else:
            try:
                while True:
                    changedFile = change_path + filename
                    tempFile = temp_path + filename

                    cv2.imwrite(tempFile, originImg, [cv2.IMWRITE_JPEG_QUALITY, quality])
                    file_size = os.path.getsize(tempFile)
                    if(file_size > targetSize ):
                        quality -= 5
                    else:
                        cv2.imwrite(changedFile, originImg, [cv2.IMWRITE_JPEG_QUALITY, quality])
                        success_cnt += 1
                        print(str(file_idx) + ". "+filename+" 변경에 성공했습니다. 변경된 파일 용량 : " + str(round(file_size/1024/1024, 1)) + "MB")
                        break
            except Exception as e:
                fail_cnt += 1
                print("[Error]다음 파일을 변환하는데 실패했습니다. 파일명 : " + filename)
                failed_file_list.append(filename)

    try:
        delete_temp_file(temp_path)
    except Exception as e:
        print("[Error]Temp 폴더 내 임시 파일들을 삭제하는데 실패했습니다.")

    print(" ")
    print("*********************** 변환 완료 ***********************")
    print("* [성공] " + str(success_cnt) + "개")
    print("* [실패] " + str(fail_cnt) + "개")

    if(fail_cnt > 0):
        print("* 변경 실패된 파일 목록은 다음과 같습니다.")
        for failed_file in failed_file_list:
            print(failed_file)
        print("---------------------------------------")

    print(" ")
    os.system("pause")

def delete_temp_file(temp_path):
    if os.path.exists(temp_path):
        for file in os.scandir(temp_path):
            os.remove(file.path)
    else:
        return 'temp derectory not found. so you cannot delete temp files'




if __name__ == '__main__':
    original_path = 'C:/moaSize/origin/'
    change_path = 'C:/moaSize/result/'
    temp_path = 'C:/moaSize/result/temp/'

    print("[Info] ------------------------- [MOA SIZE ] -------------------------------")
    print("[Info] ")
    print("[Info] 변환을 원하는 원본 파일들이 다음 경로에 있어야 합니다. [ C:/moaSize/origin ]")
    print("[Info] 변환 완료된 파일은 다음 경로에 저장됩니다. [ C:/moaSize/result ]")
    print("[Info] ")
    print("[Info] ------------------------Copyright \"Moa\"-----------------------------")
    print(" ")

    change_img_qualty(original_path, change_path, temp_path)