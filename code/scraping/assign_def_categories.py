import time
import simpleaudio as sa
import numpy as np
from PIL import Image, ImageEnhance

from scraping.adb_manipulator_utils import make_a_screenshot, big_swipe_down
from scraping.analyze_picture_utils import retrieve_text_from_image
from sql.queries import sql_execute

import nltk
from nltk.corpus import words

nltk.download('words')

list_of_categories = ['Inversion', 'Abs', 'Back', 'Beginner', 'Bodyweight', 'Calves',
                          'Chest', 'Cooldown', 'Core', 'Deadlift', 'Dips', 'Front Split',
                          'Functional', 'Hamstrings', 'Handstand', 'Handstand Press',
                          'Headstand', 'Hipflexor', 'Hips', 'Hspu', 'L-sit', 'Legs',
                          'Locomotion', 'Lower Back', 'Lunges', 'Middle Split', 'Mobility',
                          'Muscle Up', 'Neck', 'Object Manipulation', 'Pancake',
                          'Pistol Squat', 'Planche', 'Plank', 'Pull', 'Push', 'Pushup',
                          'Qdr', 'Relaxing', 'Rings', 'Shoulders Rehab', 'Shoulders',
                          'Spine', 'Squat', 'Strength', 'Stretching', 'Triceps', 'Upper Body',
                          'Warmup', 'Weighted', 'Wrist']

def get_text_from_exercise_screen():
    # make a screenshot
    make_a_screenshot()
    # crop the screenshot
    img = Image.open('../data/screenshots/temp_screen.png')
    box = img.getbbox()
    # print(box)
    rectangle = tuple([240, 710, 900, 2300])
    im_crop = img.crop(rectangle)

    # Create an enhancer object for contrast
    contrast = ImageEnhance.Contrast(im_crop)
    # Increase the contrast (1.5 times)
    new_img = contrast.enhance(3.5)
    new_img.save('../data/screenshots/temp_screen.png')

    # get the text from the screenshot
    text = retrieve_text_from_image('../data/screenshots/temp_screen.png')
    # print(text)
    return text


def get_names_and_levels_out_of_text(text):
    names_dict = {}
    print(text)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line and 'level' in line.lower():
            name=""
            # name = lines[i-3]+' '+lines[i-2]
            if i >= 3 and 'level' not in lines[i-3].lower():
                name += lines[i-3]
            if i >= 2 and 'level' not in lines[i-2].lower():
                name += ' '+lines[i-2]
            if i >= 1 and 'level' not in lines[i-1].lower():
                name += ' '+lines[i-1]
            level = line.split()[-1]
            if level.isdigit():
                names_dict[name.strip()] = int(level)
            else:
                print(f"Level is not a number: {level}")
    return names_dict


def get_names_from_screen():
    for i in range(3):
        res = get_text_from_exercise_screen()
        exercises = get_names_and_levels_out_of_text(res)
        if exercises:
            break
        else:
            print("No exercises found, trying again")
            time.sleep(2)
    return exercises


def scrape_names_from_category(category):
    exercises = {}
    ex_num = 0
    for i in range(100):
        new_exercises = get_names_from_screen()
        for i in range(6):
            big_swipe_down(pixels_down=200)

        print(new_exercises)
        # time.sleep(2.3)
        exercises.update(new_exercises)
        if len(exercises) == ex_num:
            break
        else:
            ex_num = len(exercises)
        time.sleep(3)
    return exercises, category


def play_beep_sound():
    # Set the parameters
    frequency = 440  # Frequency in Hz
    duration = 1.5  # Duration in seconds
    volume = 0.4  # Volume (0.0 to 1.0)

    # Create a numpy array for the sound wave
    t = np.linspace(0, duration, int(duration * 44100), False)
    sound_wave = volume * np.sin(frequency * 2 * np.pi * t)

    # Convert the sound wave to the correct data type for simpleaudio
    audio_data = (sound_wave * 32767).astype(np.int16)

    # Play the sound
    play_obj = sa.play_buffer(audio_data, 1, 2, 44100)

    # Wait for the sound to finish playing
    play_obj.wait_done()


def insert_exercises_to_db():
    for i, category in enumerate(list_of_categories):
        print(f"Processing category {i+1}: {category}")
        play_beep_sound()
        y = input("Continue? (y/n)")
        if 'y' not in y.lower():
            continue
        # insert category to db
        sql_execute("""INSERT OR IGNORE INTO exercise_categories (category_name)
                        VALUES (:category_name);""",
                    category_name=category)
        category_id = sql_execute("select category_id from exercise_categories where category_name=:category_name",
                    category_name=category)[0][0]
        # get list of exercises
        exercises, category = scrape_names_from_category(category)
        print(exercises)
        print("Starting to insert to db")
        # insert exercises to db
        for exercise, level in exercises.items():
            exercise = exercise.strip()
            if exercise:
                def_categories = sql_execute("select default_categories from exercises where lower(exercise_name)=:exercise_name",
                            exercise_name=exercise.lower())
                if def_categories:
                    def_categories = def_categories[0][0]
                    def_categories = def_categories.split(',')
                    if str(category_id) not in def_categories:
                        def_categories.append(str(category_id))
                        def_categories = ','.join(def_categories)
                        sql_execute("""UPDATE exercises
                                        SET default_categories = :default_categories
                                        WHERE lower(exercise_name) = :exercise_name;""",
                                    default_categories=def_categories, exercise_name=exercise.lower())
                        # print(f"Updated {exercise} to db with category {category}")
                else:
                    sql_execute("""INSERT OR IGNORE INTO exercises (exercise_name, default_categories, default_level)
                                    VALUES (:exercise_name, :default_categories, :default_level);""",
                                exercise_name=exercise, default_categories=category_id, default_level=level)
                    print(f"Inserted {exercise} to db with category {category}")


def is_english_word(word):
    return word.lower() in words.words() or word.isnumeric()


def replace_punctuation(sentence):
    return sentence.replace(',', '').replace('.', '').replace('!', '').replace('?', '').replace(';', '').replace(':', '')\
        .replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('<', '')\
        .replace('>', '').replace('/', '').replace('\\', '').replace('|', '').replace('\'', '').replace('\"', '')

def clean_scraped_exercises():
    all_exercises = sql_execute("select exercise_id, exercise_name from exercises;")
    all_exercises = sorted(all_exercises, key=lambda x: x[0])
    for ex_id, ex_name in all_exercises:
        ex_name = replace_punctuation(ex_name)
        words = ex_name.split()
        not_english = 0
        for word in words:
            if not is_english_word(word):
                not_english += 1
        if not_english > 2:
            print(f"{ex_name}")
            sql_execute("delete from exercises where exercise_id=:exercise_id", exercise_id=ex_id)
        if ex_id % 100 == 0:
            print(f"Processed {ex_id} exercises")


if __name__ == '__main__':
    # insert_exercises_to_db()
    # exercises, category = scrape_names_from_category(list_of_categories[0])
    # print(category)
    # print(exercises)

    clean_scraped_exercises()

    # print(is_english_word())

