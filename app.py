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
        start_time = time.time()
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
        end_time = time.time()
        print(f"Temps d'exécution : {end_time - start_time} secondes pour {file_path}\n")

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
