import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_snake_animation(height, width, path, blinking, save_path):
    fig, ax = plt.subplots()
    matrix = np.zeros((height, width, 3))  # 3-channel matrix for RGB color
    trail_matrix = np.zeros((height, width))  # Additional matrix to track the snake's trail
    plot = plt.imshow(matrix, interpolation='nearest')

    def fade_snake():
        # Reduce brightness of the snake
        matrix[:, :, :] *= 0.8
        # Apply minimum brightness to the snake's trail
        for x in range(height):
            for y in range(width):
                if trail_matrix[x, y] > 0:
                    matrix[x, y] = np.maximum(matrix[x, y], 0.3)

    def pulsing_red(frame, total_frames=30):
        # Calculate the phase of the pulsing (0 to 1 and back to 0)
        phase = abs((frame % (2 * total_frames)) / total_frames - 1)
        # Return the color with the pulsing intensity
        return [phase, 0, 0]

    def animate(i):
        fade_snake()  # Fade the entire snake
        # Add multiple segments of the snake in each frame
        for j in range(10 * i, min(10 * (i + 1), len(path))):
            if j < len(path):
                (x, y) = path[j].split(',')
                x, y = int(x), int(y)
                matrix[x, y] = [0, 1, 0]  # Set new positions to bright green
                trail_matrix[x, y] = 1  # Mark the trail

        # Pulsing red blocks
        for blk in blinking:
            x, y = map(int, blk.split(','))
            matrix[x, y] = pulsing_red(i)
        plot.set_array(matrix)
        return plot,

    # Adjust the total number of frames
    anim = animation.FuncAnimation(fig, animate, frames=(len(path) // 10) + 20, interval=100)
    anim.save(save_path, writer='pillow')

    plt.close(fig)
    return save_path

# Example usage
matrix_size = 20
path = [f"{np.random.randint(0, matrix_size)},{np.random.randint(0, matrix_size)}" for _ in range(80)]
blinking = ["2,4", "10,12"]
save_path = 'snake_animation.gif'
create_snake_animation(matrix_size, matrix_size, path, blinking, save_path)
