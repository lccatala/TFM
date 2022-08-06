#!/usr/bin/env python3
import matplotlib.pyplot as plt
import os

resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160), (7680, 4320)]
models = ['bmw', 'viking_room', 'sponza', 'hairball']

def plot_frametimes(filename):
    filename = f'{filename}-frametimes.txt'
    with open(filename) as f:
        lines = [int(line.rstrip()) for line in f]
        x_values = [x for x in range(1, 1000)]
        plt.figure()
        plt.plot(x_values, lines[1:-1])
        plt.savefig(f'{filename[:-4]}.png')
        plt.close()

raytraced_memory_usage_values = []
def store_raytraced_memory_usage(filename):
    filename = f'{filename}-memoryusage.txt'
    with open(filename) as f:
        value = int(f.readline())
        raytraced_memory_usage_values.append(value)

rasterized_memory_usage_values = []
def store_rasterized_memory_usage(filename):
    filename = f'{filename}-memoryusage.txt'
    with open(filename) as f:
        value = int(f.readline())
        rasterized_memory_usage_values.append(value)

def plot_memory_usage(memory_usage_values, mode):
    plt.figure()
    x_values = [x for x in range(len(memory_usage_values))]
    plt.xticks(x_values, [f'{x[0]}x{x[1]}' for x in resolutions])
    plt.bar(x_values, memory_usage_values)
    plt.savefig(f'vulkan-{mode}-memoryusage.png')
    plt.close()

def plot_rasterized():
    # modes = ['onlymodel', 'shadows', 'textures']
    path = 'VulkanRasterized2070super'
    for w, h in resolutions:
        filename_prefix = os.path.join(path, f'vulkan-{w}x{h}-rasterized')
        plot_frametimes(filename_prefix)
        store_rasterized_memory_usage(filename_prefix)
    plot_memory_usage(rasterized_memory_usage_values, 'rasterized')

def plot_raytraced():
    path = 'VulkanRaytraced2070super'
    for model in models:
        for w, h in resolutions:
            filename_prefix = os.path.join(path, f'vulkan-{w}x{h}{model}-textures')
            plot_frametimes(filename_prefix)
            store_raytraced_memory_usage(filename_prefix)
        plot_memory_usage(raytraced_memory_usage_values, f'{model}-raytraced')
        raytraced_memory_usage_values.clear()


if __name__ == '__main__':
    # plot_rasterized()
    plot_raytraced()

