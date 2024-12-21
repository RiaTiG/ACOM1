import cv2
import pytesseract
import easyocr
import os
import json
from PIL import Image
import pandas as pd
from collections import Counter
import re

pytesseract.pytesseract.tesseract_cmd = (r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe")

# img = cv2.imread('C:\\ACOM\\LR7\\yandex-capchi\\2-.jpg')
# cv2.imshow('Image', img)
# text = pytesseract.image_to_string(img, lang='rus+eng')
# print(text)
# cv2.waitKey(0)

def load_annotations(annotations_file):
    annotations = {}
    with open(annotations_file, 'r', encoding='utf-8') as f:
        for line in f:
            filename, true_text = line.strip().split('|')
            annotations[filename.strip()] = true_text.strip()
    return annotations

def test_recognition(annotations):
    results = []
    for filename, true_text in annotations.items():
        if not os.path.exists(filename):
            print(f'Файл {filename} не найден!')
            continue
        image = Image.open(filename)
        recognized_text = pytesseract.image_to_string(image)
        match = recognized_text.strip() == true_text.strip()
        results.append({
            'filename': filename,
            'recognized': recognized_text.strip(),
            'true': true_text.strip(),
            'match': match
        })
    results_df = pd.DataFrame(results)
    print(f'Обработано изображений: {len(results_df)}, Найдено совпадений: {results_df["match"].sum()}')
    return results_df

def augment_dataset(annotations, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    augmentations = []
    for filename, true_text in annotations.items():
        if not os.path.exists(filename):
            print(f'Файл {filename} не найден для аугментации!')
            continue
        image = Image.open(filename)

        for angle in range(-20, 21):
            rotated_image = image.rotate(angle)
            rotated_filename = f"{os.path.splitext(os.path.basename(filename))[0]}_rot{angle}.jpg"
            rotated_image.save(os.path.join(output_dir, rotated_filename))
            augmentations.append((os.path.join(output_dir, rotated_filename), true_text))
    print(f'Всего аугментированных файлов: {len(augmentations)}')
    return augmentations

def cleanup_text(text):
    cleaned = ''.join(filter(str.isalnum, text)).lower()
    return cleaned

def new_recognition_method(filename, true_text=None):
    if true_text is None:
        true_text = original_annotations.get(filename)
    if true_text is None:
        print(f'Истинный текст не найден для файла: {filename}')
        return None
    if not os.path.exists(filename):
        print(f'Файл {filename} не найден для нового метода!')
        return None
    image = Image.open(filename)
    recognized_text = pytesseract.image_to_string(image)
    cleaned_recognized_text = cleanup_text(recognized_text.strip())
    match = cleaned_recognized_text == cleanup_text(true_text.strip())
    return {
        'filename': filename,
        'recognized': cleaned_recognized_text,
        'true': cleanup_text(true_text.strip()),
        'match': match
    }


annotations_file = 'C:\\ACOM\\LR7\\annotation.txt'
original_annotations = load_annotations(annotations_file)
results_df = test_recognition(original_annotations)
results_df.to_csv('original_results.csv', index=False, encoding='utf-8')

output_dir = 'augmented_dataset'
augmented_annotations = augment_dataset(original_annotations, output_dir)
augmented_df = test_recognition({filename: true_text for filename, true_text in augmented_annotations})
augmented_df.to_csv('augmented_results.csv', index=False, encoding='utf-8')

summary_df = pd.DataFrame({
    'Original Total': [len(original_annotations)],
    'Original Correct': [results_df['match'].sum()],
    'Original Accuracy': [results_df['match'].mean() * 100],
    'Augmented Total': [len(augmented_annotations)],
    'Augmented Correct': [augmented_df['match'].sum() if 'match' in augmented_df.columns else 0],
    'Augmented Accuracy': [augmented_df['match'].mean() * 100 if 'match' in augmented_df.columns else 0]
})
summary_df.to_csv('summary_results.csv', index=False, encoding='utf-8')

results_new_method = []
for filename in original_annotations.keys():
    result = new_recognition_method(filename)
    if result:
        results_new_method.append(result)
results_new_method_df = pd.DataFrame(results_new_method)
results_new_method_df.to_csv('new_method_results_original.csv', index=False, encoding='utf-8')

results_new_method_augmented = []
for filename, true_text in augmented_annotations:
    result = new_recognition_method(filename, true_text=true_text) 
    if result:
        results_new_method_augmented.append(result)
results_new_method_augmented_df = pd.DataFrame(results_new_method_augmented)
results_new_method_augmented_df.to_csv('new_method_results_augmented.csv', index=False, encoding='utf-8')

# 3
# def load_annotations(annotations_file):
#     annotations = {}
#     with open(annotations_file, 'r', encoding='utf-8') as f:
#         for line in f:
#             filename, true_text = line.strip().split('|')
#             annotations[filename.strip()] = true_text.strip()
#     return annotations


# def augment_image(image):
#     augmented_images = []
#     for angle in range(-20, 21):
#         rotated_image = image.rotate(angle)
#         augmented_images.append(rotated_image)
#     return augmented_images


# def get_final_result(texts):
#     counts = Counter(texts)
#     most_common_text, _ = counts.most_common(1)[0]
#     return most_common_text


# def test_recognition_with_augmentation(annotations):
#     results = []

#     for filename, true_text in annotations.items():
#         if not os.path.exists(filename):
#             print(f'Файл {filename} не найден!')
#             continue

#         image = Image.open(filename)
#         augmented_images = augment_image(image)

#         recognized_texts = []
#         for aug_image in augmented_images:
#             recognized_text = pytesseract.image_to_string(aug_image).strip()
#             recognized_texts.append(recognized_text)
#             print(f'Изображение {filename}, повернутое на {aug_image}, распознано как: "{recognized_text}"')

#         print(f'Все распознанные тексты для файла {filename}: {recognized_texts}')
#         final_result = get_final_result(recognized_texts)
#         print(f'Итоговый результат для файла {filename}: "{final_result}"')
#         match = final_result == true_text.strip()
#         results.append({
#             'filename': filename,
#             'final_result': final_result,
#             'true_text': true_text.strip(),
#             'match': match
#         })

#     results_df = pd.DataFrame(results)
#     print(f'Обработано изображений: {len(results_df)}, Найдено совпадений: {results_df["match"].sum()}')  # Для отладки
#     return results_df

# annotations_file = 'C:\\ACOM\\LR7\\annotation.txt'
# original_annotations = load_annotations(annotations_file)
# results_df = test_recognition_with_augmentation(original_annotations)
# results_df.to_csv('new_method_results.csv', index=False, encoding='utf-8')

# summary_df = pd.DataFrame({
#     'Total Images': [len(original_annotations)],
#     'Correct Matches': [results_df['match'].sum()],
#     'Accuracy (%)': [results_df['match'].mean() * 100],
# })
# summary_df.to_csv('new_method_summary.csv', index=False, encoding='utf-8')

# 5
# Переобучение Тессеракта рот ебал
# custom_oem_psm_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# custom_lang = "new_trained_mode"
# def load_annotations(annotations_file):
#     annotations = {}
#     with open(annotations_file, 'r', encoding='utf-8') as f:
#         for line in f:
#             filename, true_text = line.strip().split('|')
#             annotations[filename.strip()] = true_text.strip()
#     return annotations
# def cleanup_text(text):
#     cleaned = re.sub(r'[^а-яА-ЯёЁa-zA-Z0-9\s]', '', text)
#     return cleaned.lower()
# def test_recognition_with_cleanup(annotations):
#     results = []
#     for filename, true_text in annotations.items():
#         if not os.path.exists(filename):
#             print(f'Файл {filename} не найден!')
#             continue
#         image = Image.open(filename)
#         recognized_text = pytesseract.image_to_string(image, lang=custom_lang, config=custom_oem_psm_config)
#         cleaned_text = cleanup_text(recognized_text.strip())
#         match = cleaned_text == cleanup_text(true_text.strip())
#         results.append({
#             'filename': filename,
#             'recognized_text': cleaned_text,
#             'true_text': cleanup_text(true_text.strip()),
#             'match': match
#         })
#     results_df = pd.DataFrame(results)
#     print(f'Обработано изображений: {len(results_df)}, Найдено совпадений: {results_df["match"].sum()}')  # Для отладки
#     return results_df
# annotations_file = 'C:\\ACOM\\LR7\\annotation.txt'
# original_annotations = load_annotations(annotations_file)
# annotations_file2 = 'C:\\ACOM\\LR7\\annotation2.txt'
# dataset2_annotations = load_annotations(annotations_file2)
# results_df_original = test_recognition_with_cleanup(original_annotations)
# results_df_dataset2 = test_recognition_with_cleanup(dataset2_annotations)
# results_df_original.to_csv('original_results_after_training.csv', index=False, encoding='utf-8')
# results_df_dataset2.to_csv('dataset2_results_after_training.csv', index=False, encoding='utf-8')


# 6
# reader = easyocr.Reader(['ru'])
# def test_easyocr(dataset_path):
#     results = []
#     for filename in os.listdir(dataset_path):
#         if filename.endswith('.jpg') or filename.endswith('.png'):
#             image_path = os.path.join(dataset_path, filename)
#             result = reader.readtext(image_path)
#             recognized_text = ' '.join([item[1] for item in result])
#             print(f'Recognized text for {filename}: {recognized_text}')
#             results.append({'filename': filename, 'recognized_text': recognized_text,
#                             'accuracy': None})
#     return results

# dataset1_path = 'C:\\ACOM\\LR7\\yandex-capchi'
# dataset2_path = 'augmented_dataset'
# results_dataset1 = test_easyocr(dataset1_path)
# results_dataset2 = test_easyocr(dataset2_path)
# summary_df = pd.DataFrame(results_dataset1 + results_dataset2)