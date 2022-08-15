import tqdm
import subprocess

def main():
	resolutions = [('1280', '720'), ('1920', '1080'), ('2560', '1440'), ('3840', '2160'), ('7680', '4320')]	
	models = ['bmw', 'sponza', 'hairball']
	executables = ['vk_ray_tracing__simple_KHR.exe']
	for w, h in tqdm.tqdm(resolutions):
		for exe in executables:
			for model in models:
				subprocess.run([f'{exe}', f'{w}', f'{h}', f'{model}'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
if __name__ == '__main__':
	main()
