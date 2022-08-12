#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import os


resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]
models = ['bmw', 'sponza', 'hairball']

def plot_frametimes(filename, include_first=False):
    filename = f'{filename}-frametimes.txt'
    with open(filename) as f:
        lines = [int(line.rstrip()) for line in f]
        start = 0 if include_first else 1
        x_values = [x for x in range(start, 1000)]
        plt.figure()
        plt.plot(x_values, lines[start:-1])
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

def plot_raytraced(include_first=False):
    path = 'VulkanRaytraced2070super'
    for model in models:
        for w, h in resolutions:
            filename_prefix = os.path.join(path, f'vulkan-{w}x{h}{model}-textures')
            plot_frametimes(filename_prefix, include_first=include_first)
            store_raytraced_memory_usage(filename_prefix)
        plot_memory_usage(raytraced_memory_usage_values, f'{model}-raytraced')
        raytraced_memory_usage_values.clear()

def read_value(filename):
    with open(filename) as f:
        value = float(f.readlines()[-1])
        return value

def plot_compared_memory_usages():
    rasterized_path = 'VulkanRasterized2070super'
    raytraced_path = 'VulkanRaytraced2070super'
    model = 'viking_room'
    rasterized_memory_usages = []
    raytraced_memory_usages = []
    for w, h in resolutions:
        filename = os.path.join(rasterized_path, f'vulkan-{w}x{h}-rasterized-memoryusage.txt')
        rasterized_memory_usages.append(read_value(filename))

        filename = os.path.join(raytraced_path, f'vulkan-{w}x{h}{model}-textures-memoryusage.txt')
        raytraced_memory_usages.append(read_value(filename))

    labels = [f'{x[0]}x{x[1]}' for x in resolutions]
    x = np.arange(len(labels))
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width/2, rasterized_memory_usages, bar_width, label='Rasterized')
    rects2 = ax.bar(x + bar_width/2, raytraced_memory_usages, bar_width, label='Raytraced')

    ax.set_ylabel('Memory (MB)')
    ax.set_title('Memory usage for rasterized and raytraced rendering')
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('vulkan-memory-usage-comparison.png')

def plot_compared_raytraced_memory_usages():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for model in models:
        optix_memory_usages = []
        vulkan_memory_usages = []
        for w, h in resolutions:
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-memoryusage.txt')
            optix_memory_usages.append(read_value(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-memoryusage.txt')
            vulkan_memory_usages.append(read_value(filename))

        labels = [f'{x[0]}x{x[1]}' for x in resolutions]
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_memory_usages, bar_width, label='Vulkan')
        rects1 = ax.bar(x - bar_width/2, optix_memory_usages, bar_width, label='OptiX')

        ax.set_ylabel('Memory (MB)')
        ax.set_title(f'Memory usage for raytraced rendering of {model} model')
        ax.set_xticks(x, labels)
        ax.legend()
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()
        plt.savefig(f'{model}-memory-usage-comparison.png')

def plot_compared_raytraced_frametimes():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for model in models:
        optix_frametimes = []
        vulkan_frametimes = []
        for w, h in resolutions: # TODO
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-frametimes.txt')
            optix_frametimes.append(read_value(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-frametimes.txt')
            vulkan_frametimes.append(read_value(filename))

        labels = [f'{x[0]}x{x[1]}' for x in resolutions]
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_frametimes, bar_width, label='Vulkan')
        rects1 = ax.bar(x - bar_width/2, optix_frametimes, bar_width, label='OptiX')

        ax.set_ylabel('Frame times (microseconds)')
        ax.set_title(f'Frame time for raytraced rendering of {model} model')
        ax.set_xticks(x, labels)
        ax.legend()
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()
        plt.savefig(f'{model}-frametimes-comparison.png')
def plot_compared_frame_times():
    rasterized_path = 'VulkanRasterized2070super'
    raytraced_path = 'VulkanRaytraced2070super'
    model = 'viking_room'
    rasterized_frametimes = []
    raytraced_frametimes = []
    for w, h in resolutions:
        filename = os.path.join(rasterized_path, f'vulkan-{w}x{h}-rasterized-frametimes.txt')
        rasterized_frametimes.append(read_value(filename))

        filename = os.path.join(raytraced_path, f'vulkan-{w}x{h}{model}-textures-frametimes.txt')
        raytraced_frametimes.append(read_value(filename))

    labels = [f'{x[0]}x{x[1]}' for x in resolutions]
    x = np.arange(len(labels))
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width/2, rasterized_frametimes, bar_width, label='Rasterized')
    rects2 = ax.bar(x + bar_width/2, raytraced_frametimes, bar_width, label='Raytraced')

    ax.set_ylabel('Frame time (microseconds)')
    ax.set_title('Frame render times for rasterized and raytraced rendering')
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('vulkan-frametimes-comparison.png')

def plot_compared_raytraced_as_build_times():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for model in models:
        optix_as_build_times = []
        vulkan_build_times = []
        for w, h in resolutions:
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-accelbuildtime.txt')
            optix_as_build_times.append(read_value(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-accelbuildtime.txt')
            vulkan_build_times.append(read_value(filename))

        labels = [f'{x[0]}x{x[1]}' for x in resolutions]
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_build_times, bar_width, label='Vulkan')
        rects1 = ax.bar(x - bar_width/2, optix_as_build_times, bar_width, label='OptiX')

        ax.set_ylabel('AS Build Time (microseconds)')
        ax.set_title(f'AS Build Time for raytraced rendering of {model} model')
        ax.set_xticks(x, labels)
        ax.legend()
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()
        plt.savefig(f'{model}-acceleration-structure-build-time-comparison.png')

def plot_compared_raytraced_as_build_times_geometry():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for w, h in resolutions:
        optix_as_build_times = []
        vulkan_build_times = []
        for model in models:
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-accelbuildtime.txt')
            optix_as_build_times.append(read_value(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-accelbuildtimes.txt')
            with open(filename) as f:
                values = [int(x) for x in f.readlines()]
                avg = sum(values) / len(values)
                vulkan_build_times.append(avg)
                print(avg)

        labels = models
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_build_times, bar_width, label='Vulkan')
        rects1 = ax.bar(x - bar_width/2, optix_as_build_times, bar_width, label='OptiX')

        ax.set_ylabel('AS Build Time (microseconds)')
        ax.set_title(f'AS Build Time for raytraced rendering at resolution {w}x{h}')
        ax.set_xticks(x, labels)
        ax.legend()
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()
        plt.savefig(f'{w}x{h}-acceleration-structure-geometry-build-time-comparison.png')
if __name__ == '__main__':
    # plot_rasterized()
    # plot_raytraced(include_first=False)
    # plot_raytraced(include_first=True)
    # plot_compared_memory_usages()
    # plot_compared_frame_times()
    # plot_compared_raytraced_memory_usages()
    plot_compared_raytraced_frametimes()
    # plot_compared_raytraced_as_build_times_geometry()
