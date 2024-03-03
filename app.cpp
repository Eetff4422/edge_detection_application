#include <iostream>
#include <fstream>
#include <filesystem>
#include <opencv2/opencv.hpp>

namespace fs = std::filesystem;

class EdgeDetector {
public:
    EdgeDetector(std::string data_folder, double threshold1, double threshold2) 
        : data_folder(data_folder), threshold1(threshold1), threshold2(threshold2) {}

    void process_folders() {
        for (const auto& entry : fs::directory_iterator(data_folder)) {
            const auto& path = entry.path();
            if (path.filename() == "input") {
                std::string input_folder = path.string();
                std::string output_folder = input_folder.replace(input_folder.find("input"), 5, "output");

                if (!fs::exists(output_folder)) {
                    fs::create_directories(output_folder);
                    std::cout << "Dossier créé : " << output_folder << std::endl;
                }

                for (const auto& file_entry : fs::directory_iterator(input_folder)) {
                    process_file(file_entry.path().string(), output_folder);
                    std::cout << "Traitement terminé pour : " << file_entry.path().string() << std::endl;
                }
            }
        }
    }

private:
    std::string data_folder;
    double threshold1, threshold2;

    void process_file(const std::string& file_path, const std::string& output_folder) {
        if (file_path.ends_with(".jpg") || file_path.ends_with(".png")) {
            cv::Mat image = cv::imread(file_path, cv::IMREAD_GRAYSCALE);
            if (image.empty()) {
                throw std::runtime_error("L'image spécifiée par " + file_path + " n'a pas pu être chargée.");
            }
            cv::Mat edges;
            cv::Canny(image, edges, threshold1, threshold2);
            std::string output_path = output_folder + "/" + fs::path(file_path).filename().string();
            cv::imwrite(output_path, edges);
        } else if (file_path.ends_with(".mp4")) {
            cv::VideoCapture cap(file_path);
            if (!cap.isOpened()) {
                throw std::runtime_error("La vidéo spécifiée par " + file_path + " n'a pas pu être chargée.");
            }
            int frame_width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
            int frame_height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
            cv::VideoWriter out(output_folder + "/" + fs::path(file_path).filename().string(), 
                                cv::VideoWriter::fourcc('m', 'p', '4', 'v'), 
                                20, 
                                cv::Size(frame_width, frame_height), 
                                false);

            cv::Mat frame, edges;
            while (true) {
                cap >> frame;
                if (frame.empty()) {
                    break;
                }
                cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
                cv::Canny(frame, edges, threshold1, threshold2);
                out.write(edges);
            }
            cap.release();
            out.release();
        }
    }
};

int main() {
    std::string data_folder = "data";
    double threshold1 = 100;
    double threshold2 = 200;

    EdgeDetector detector(data_folder, threshold1, threshold2);
    detector.process_folders();

    return 0;
}
