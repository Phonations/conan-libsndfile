import os

from conans import ConanFile, CMake, tools


class LibsndfileTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        bin_path = os.path.join("bin", "example")
        wav_path = os.path.join(self.source_folder, "Alesis-Fusion-Clean-Guitar-C3.wav")
        self.run("{} {}".format(bin_path, wav_path), run_environment=True)
