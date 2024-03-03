# # import cv2
# # import time

# # def apply_canny_edge_detector(list_image_path, threshold1, threshold2):
# #     start_time = time.time()
# #     # Charger l'image
# #     for img in list_image_path:
# #         image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
# #         if image is None:
# #             raise FileNotFoundError(f"L'image spécifiée par {img} n'a pas pu être chargée.")

# #         # Appliquer le détecteur de bords de Canny
# #         edges = cv2.Canny(image, threshold1, threshold2)

# #         # Sauvegarder le résultat
# #         output_path = 'edges_' + img.split('/')[-1]
# #         cv2.imwrite(output_path, edges)
# #         print(f"L'image traitée a été sauvegardée sous : {output_path}")

# #         end_time = time.time()
# #         print(f"Temps d'exécution : {end_time - start_time} secondes pour l'image {img}\n")
# #         #return output_path

# # if __name__ == "__main__":
# #     # import sys
# #     # if len(sys.argv) != 4:
# #     #     print("Usage: python script.py <path_to_image> <threshold1> <threshold2>")
# #     #     sys.exit(1)

# #     list_image_path = ["pexels-diana-light-20073934.jpg","pexels-roger-brown-14974522.jpg","pexels-efrem-efre-20424669.jpg"]
# #     threshold1 = 100
# #     threshold2 = 200
    
# #     apply_canny_edge_detector(list_image_path, threshold1, threshold2)
# import cv2
# import time

# def apply_canny_edge_detector(list_media_paths, threshold1, threshold2):
#     for media in list_media_paths:
#         start_time = time.time()
        
#         if media.endswith('.jpg') or media.endswith('.png'):  # Vérifier si le fichier est une image
#             image = cv2.imread(media, cv2.IMREAD_GRAYSCALE)
#             if image is None:
#                 raise FileNotFoundError(f"L'image spécifiée par {media} n'a pas pu être chargée.")

#             edges = cv2.Canny(image, threshold1, threshold2)
#             output_path = 'edges_' + media.split('/')[-1]
#             cv2.imwrite(output_path, edges)

#         elif media.endswith('.mp4'):  # Vérifier si le fichier est une vidéo
#             cap = cv2.VideoCapture(media)
#             fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # ou 'XVID' si le format .avi est préféré
#             out = cv2.VideoWriter('edges_' + media.split('/')[-1], fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))), False)

#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if ret:
#                     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                     edges = cv2.Canny(gray, threshold1, threshold2)
#                     out.write(edges)
#                 else:
#                     break
#             cap.release()
#             out.release()
        
#         end_time = time.time()
#         print(f"Temps d'exécution : {end_time - start_time} secondes pour {media}\n")

# if __name__ == "__main__":
#     list_media_paths = [
#         "pictures/input/pexels-diana-light-20073934.jpg",
#         "pictures/input/pexels-roger-brown-14974522.jpg",
#         "pictures/input/pexels-efrem-efre-20424669.jpg",
#         "videos/input/coverr-ai-generated-aerial-view-of-a-dubai-like-modern-cityscape-1080p.mp4",
#         "videos/input/coverr-an-australian-shepherd-in-the-city-5619-1080p.mp4",
#         "videos/input/coverr-a-guy-scrolls-photos-on-his-smartphone-9855-1080p.mp4"
#     ]
#     threshold1 = 100
#     threshold2 = 200
    
#     apply_canny_edge_detector(list_media_paths, threshold1, threshold2)

import cv2
import os
import time

class EdgeDetector:
    def __init__(self, data_folder, threshold1, threshold2):
        self.data_folder = data_folder
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    @staticmethod
    def ensure_folder_exists(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Dossier créé : {folder_path}")

    def process_file(self, file_path, output_folder):
        # Vérifier l'extension du fichier pour déterminer le traitement
        if file_path.endswith(('.jpg', '.png')):
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                raise FileNotFoundError(f"L'image spécifiée par {file_path} n'a pas pu être chargée.")
            edges = cv2.Canny(image, self.threshold1, self.threshold2)
            output_path = os.path.join(output_folder, os.path.basename(file_path))
            cv2.imwrite(output_path, edges)
        elif file_path.endswith('.mp4'):
            cap = cv2.VideoCapture(file_path)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(os.path.join(output_folder, os.path.basename(file_path)), fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))), False)

            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, self.threshold1, self.threshold2)
                    out.write(edges)
                else:
                    break
            cap.release()
            out.release()

    def process_folders(self):
        for root, dirs, files in os.walk(self.data_folder):
            for dir_name in dirs:
                if dir_name == 'input':
                    input_folder = os.path.join(root, dir_name)
                    output_folder = input_folder.replace('input', 'output')
                    self.ensure_folder_exists(output_folder)  # Crée le dossier de sortie si nécessaire

                    for file in os.listdir(input_folder):
                        file_path = os.path.join(input_folder, file)
                        self.process_file(file_path, output_folder)
                        print(f"Traitement terminé pour : {file_path}")

if __name__ == "__main__":
    # Paramètres de configuration
    data_folder = "data"
    threshold1 = 100
    threshold2 = 200
    
    # Création et exécution du détecteur de bords
    detector = EdgeDetector(data_folder, threshold1, threshold2)
    detector.process_folders()
