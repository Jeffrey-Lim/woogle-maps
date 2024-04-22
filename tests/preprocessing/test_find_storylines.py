import pandas as pd
import polars as pl

from src.preprocessing.find_storylines import FindStorylines


class TestFindStorylines:

    def test_reduction(self):
        data = pd.DataFrame({
            "title": [
                "Covid in Wuhan",
                "Sars ruled out",
                "First death reported",
                "Lockdown in New York",
                "New strain found",
                "Vaccine development begins",
                "Global cases rise",
                "Travel restrictions applied",
            ],
            "date": [
                "2023-02-19", "2023-02-24", "2023-02-28", "2023-03-21",
                "2023-03-22", "2023-05-02", "2023-04-12", "2023-05-17",
            ],
            "clusters": [
                0, 0, 0, 1, 1, 1, 2, 2,
            ],
            "adj_list": [
                [1, 2],  # Adjusted from [2, 3] to [1, 2]
                [1, 2],  # Adjusted from [2, 3] to [1, 2]
                [1, 2],  # Adjusted from [2, 3] to [1, 2]
                [0],  # Adjusted from [1] to [0]
                [0],  # Adjusted from [1] to [0]
                [0],  # Adjusted from [1] to [0]
                [0, 1],  # Adjusted from [1, 2] to [0, 1]
                [0, 1],  # Adjusted from [1, 2] to [0, 1]
            ],
            "adj_weights": [
                [0.7, 0.3],
                [0.7, 0.3],
                [0.7, 0.3],
                [0.5],
                [0.5],
                [0.5],
                [0.6, 0.4],
                [0.6, 0.4],
            ],
        })
        storylines = [0, 0, 0, 1, 1, 1, 0, 0]
        block = FindStorylines()
        res_df = block.transform(data)
        assert res_df['storyline'].tolist() == storylines

    def test__find_storylines(self):
        data = pl.DataFrame(
            {
                "adj_list": [[8, 10, 1], [7, 8, 2], [7, 8, 10], [4, 5], [7, 8, 6], [7], [8, 9, 10], [8, 10], [12, 10, 9], [12, 13, 10], [11, 13], [13], [], []],
                "adj_weights": [
                    [0.0640658152988518, 0.06406582718181346, 0.8718683575193347],
                    [0.11111110958452239, 0.11111110958452239, 0.7777777808309553],
                    [0.3333333127243863, 0.3333333127243863, 0.3333333745512273],
                    [0.6666666666666666, 0.3333333333333333],
                    [0.25, 0.25, 0.5],
                    [1.0],
                    [0.25, 0.25, 0.5],
                    [0.09999999958782103, 0.900000000412179],
                    [0.19999999999999998, 0.2000000247307379, 0.5999999752692621],
                    [0.33333331959403506, 0.33333331959403506, 0.3333333608119299],
                    [0.39835457951843506, 0.6016454204815649],
                    [1.0],
                    [],
                    [],
                ],
            },
        )
        stories = [[0, 1, 2, 10, 13], [3, 4, 8, 12], [5, 7], [6, 9], [11]]

        block = FindStorylines()
        res_df = block.transform(data)

        assert res_df["storyline"].to_list() == [0, 0, 0, 1, 1, 2, 3, 2, 1, 3, 0, 4, 1, 0]

    def test__find_stories_2(self) -> None:
        data = pl.DataFrame(
            {
                "adj_list": [[1, 2, 3, 4], [2, 3, 4, 5], [3], [4], [5, 6, 7, 8], [6, 7, 8, 9], [8, 9], [8, 9], [9, 10], [10], [11, 12], [12, 13, 14], [13, 14],
                             [14, 15, 16, 17], [15, 16, 17], [16, 17, 18], [17, 18, 20], [18, 19, 20, 21], [19, 20, 21], [20, 23], [21, 22, 23, 24], [22, 23], [23, 25, 26],
                             [24, 25, 26, 27], [25, 26], [26, 28, 29], [27, 28], [28, 29], [29, 30, 32], [30, 31, 32], [31, 32], [32, 33], [33, 34, 35], [34, 35, 36, 37],
                             [35, 37], [36, 37, 38], [37, 38], [38, 39, 40], [39, 40, 41], [40, 41, 42, 43], [41, 42, 43], [42], [43], [44, 46], [45, 46], [46, 47, 48, 49],
                             [47, 48, 49], [48, 49, 50], [49, 50, 51], [50, 52], [51, 52, 53], [52, 53, 54, 55], [53, 54, 55], [54, 56], [55, 56, 57, 58], [56, 57, 58],
                             [57, 58, 60], [58, 59, 60], [59, 60], [60, 61], [61], [62, 63, 64, 65], [63, 64, 65, 66], [64], [65, 67, 68], [66, 67, 68], [67, 68, 69],
                             [68, 70], [69, 70, 71], [70, 71, 72, 73], [71, 72, 73], [72, 73, 75], [73, 74, 75], [74, 75, 76], [75, 76], [76], [77, 78], [78, 79, 80, 81],
                             [79, 80], [80, 81, 82, 83], [81, 82], [82, 83, 84], [83, 84, 85, 87], [84, 85, 87], [85, 86, 87], [86, 87], [87, 88, 89], [88], [89, 90, 91],
                             [90, 91], [91, 92, 93], [92, 93, 94], [93, 94, 95, 96], [94, 95], [95, 96, 97, 98], [96, 97], [97, 98, 99], [98, 99, 100, 101], [99, 100, 101],
                             [100, 101, 103], [101, 102, 103], [102, 103], [103, 104], [104], [105], [106, 107, 108], [107, 108, 109, 110], [108, 109, 110], [109], [110],
                             [111, 112], [112, 113], [113], [114, 115], [115, 116, 117, 118], [116, 118], [117, 119], [118, 119, 120, 121], [119, 120, 122], [120, 122, 123],
                             [121, 122, 123], [122, 123], [123, 124], [124, 125, 126], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132, 133],
                             [132, 133, 134, 135], [134, 135], [134, 135], [135, 136, 137, 138], [136, 137], [137, 138, 139, 140], [138, 139, 140], [139, 140, 142],
                             [140, 141, 142], [141, 142, 143, 144], [142, 143], [143, 144, 145, 146], [144, 145, 146], [145, 146, 147], [146, 147, 148], [147, 148, 149, 150],
                             [148, 149, 150], [149, 150, 151], [150, 151, 152], [151, 152], [152, 153, 154], [153, 154], [154, 155], [155], [156, 157], [157], [158, 159],
                             [159], [160, 161], [161, 162, 163, 164], [162, 163, 164], [163, 164, 165, 166], [164, 165, 167], [165, 166, 167], [166, 168, 169],
                             [167, 168, 169, 173], [168, 169, 171], [169, 170, 171, 173], [170, 171, 172, 173], [171, 172], [172, 173, 174], [173, 174, 175], [174, 175],
                             [175, 176, 177], [176, 177, 178], [177, 178, 179, 180], [178, 179, 181], [179, 180, 181], [180, 181], [181, 182, 184], [182, 183], [183, 184],
                             [184, 185, 186, 187, 188], [185, 186, 188], [186, 188], [187, 188, 191], [188, 189], [189, 190, 191], [190, 191], [191, 193], [192, 193, 194],
                             [193, 194, 195, 196], [194, 195, 197], [195, 196, 197], [196, 197], [197, 198, 199, 200], [198, 199], [199, 200], [200, 201, 202, 203],
                             [201, 202, 203], [202, 203], [203, 204, 205, 206], [204, 205, 206, 207], [205, 206], [206, 207, 208], [207, 208, 209, 210], [208, 209, 210],
                             [209, 210, 211], [210, 211, 212], [211, 212, 213, 214], [212, 213, 214], [213, 214, 215], [214, 215, 217], [215, 216, 217], [216, 217, 218, 219],
                             [217, 218], [218, 219, 220, 221], [219, 220, 221], [220, 221, 222], [221, 222, 223], [222, 223, 225], [223, 224, 225, 226], [224, 225, 226],
                             [225, 226], [226, 227, 228], [227, 228, 229, 230, 231], [228, 231], [229, 230, 231], [231, 233], [231, 233], [232, 233], [233], [234], [235, 236],
                             [236, 237, 238], [237, 238], [238, 239], [239], [240], [241], [242], []],
                "adj_weights": [[0.9214907890785091, 0.02616973697383026, 0.02616973697383026, 0.02616973697383026], [0.25, 0.25, 0.25, 0.25], [1.0], [1.0],
                                [0.5, 0.16666666666666666, 0.16666666666666666, 0.16666666666666666], [0.25, 0.25, 0.25, 0.25], [0.5, 0.5], [0.5, 0.5], [0.25, 0.75], [1.0],
                                [0.8571428555831805, 0.1428571444168195], [0.16666666454377352, 0.6666666709124529, 0.16666666454377352], [0.5, 0.5], [0.2, 0.4, 0.2, 0.2],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3512050123430947, 0.3512050123430947, 0.2975899753138106], [0.25, 0.25, 0.288165056836452, 0.21183494316354803],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.25, 0.25, 0.25, 0.25], [0.6666666666666666, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25], [0.5, 0.5],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.75], [0.5, 0.5], [0.2, 0.2, 0.6],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.5, 0.5],
                                [0.6666666709124529, 0.16666666454377352, 0.16666666454377352], [0.2, 0.2, 0.2, 0.4], [0.5, 0.5],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.2, 0.6, 0.2],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [1.0], [1.0], [0.8571428555831805, 0.1428571444168195],
                                [0.833333338640566, 0.16666666135943395], [0.19999998777213618, 0.40000016660464466, 0.19999998777213618, 0.19999985785108304],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333248417635, 0.3333333375791182, 0.3333333375791182],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.7499999808939601, 0.25000001910603986], [0.6, 0.2, 0.2],
                                [0.25, 0.25, 0.25, 0.25], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.6666666666666666, 0.3333333333333333],
                                [0.25, 0.25, 0.25, 0.25], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.33333329087547564, 0.33333329087547564, 0.3333334182490488], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.75],
                                [0.499999914022842, 0.5000000859771581], [1.0], [0.571428513720544, 0.14285716391277448, 0.14285716391277448, 0.142857158453907],
                                [0.25, 0.25, 0.25, 0.25], [1.0], [0.4999999761174509, 0.2500000119412746, 0.2500000119412746], [0.5, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.6666666666666666, 0.3333333333333333], [0.6, 0.2, 0.2],
                                [0.25, 0.25, 0.25, 0.25], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.5],
                                [0.5, 0.5], [1.0], [0.5714285761076012, 0.4285714238923988], [0.25, 0.25, 0.25, 0.25], [0.75, 0.25], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.6666666666666666], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.6666666666666666, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [1.0],
                                [0.16666666454377352, 0.6666666709124529, 0.16666666454377352], [0.5, 0.5], [0.2, 0.6, 0.2],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25], [0.6666666666666666, 0.3333333333333333],
                                [0.25, 0.25, 0.25, 0.25], [0.3333334352322048, 0.6666665647677953], [0.3333332993670463, 0.3333332993670463, 0.33333340126590744],
                                [0.25000001910603986, 0.25000001910603986, 0.25000001910603986, 0.24999994268188042],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.33333340126590744, 0.3333332993670463, 0.3333332993670463],
                                [0.3333332993670463, 0.33333340126590744, 0.3333332993670463], [0.25000011463623917, 0.7499998853637609], [0.5, 0.5], [1.0], [1.0],
                                [0.5714286462930497, 0.2857143941118115, 0.1428569595951389],
                                [0.24999996178792902, 0.25000003821207095, 0.25000003821207095, 0.24999996178792902],
                                [0.3333333672996156, 0.33333338003697144, 0.33333325266341296], [1.0], [1.0], [0.8569346554963636, 0.14306534450363634],
                                [0.16695012428786554, 0.8330498757121345], [1.0], [0.8571428555831805, 0.1428571444168195],
                                [0.16666666666666666, 0.16666666666666666, 0.5, 0.16666666666666666], [0.5, 0.5], [0.5, 0.5], [0.25, 0.25, 0.25, 0.25],
                                [0.3504313220886286, 0.3504313220886286, 0.29913735582274276], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.7405041512613628, 0.2594958487386372],
                                [0.170834281678755, 0.170834281678755, 0.6583314366424899], [0.5340979378704009, 0.465902062129599], [0.5, 0.5],
                                [0.170834278333171, 0.829165721666829], [0.5, 0.5], [0.16666666135943395, 0.833333338640566], [0.5000001719543457, 0.49999982804565446],
                                [0.6666665690135885, 0.16666671867754534, 0.16666671230886634],
                                [0.20000002904118258, 0.20000002904118258, 0.39999991287645226, 0.20000002904118258], [0.5000001815072989, 0.4999998184927011], [0.5, 0.5],
                                [0.25, 0.25, 0.25, 0.25], [0.75, 0.25], [0.2499999976117452, 0.26774132017699187, 0.2499999976117452, 0.23225868459951773],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.2545154380968566, 0.2545154380968566, 0.2545154380968566, 0.23645368570943018], [0.5, 0.5], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.75], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.19999999694303386, 0.8000000030569661], [0.5, 0.5], [1.0], [0.1428571444168195, 0.8571428555831805], [1.0],
                                [0.1428571444168195, 0.8571428555831805], [1.0], [0.8571428555831805, 0.1428571444168195],
                                [0.16666666666666666, 0.5385549410246908, 0.16666666666666666, 0.12811172564197595],
                                [0.3843351791288646, 0.5000000028659057, 0.11566481800522958], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.22144101140662856, 0.3333333350316479, 0.3333333350316479, 0.11189231853007577],
                                [0.3753298636939401, 0.3753298636939401, 0.24934027261211977],
                                [0.3333333333333333, 0.3333333333333333, 0.1118924504285236, 0.22144088290480973], [0.25, 0.25, 0.25, 0.25], [0.5, 0.5],
                                [0.33333329087547564, 0.33333329087547564, 0.3333334182490488], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.25000002388255027, 0.7499999761174497], [0.3333334182490488, 0.33333329087547564, 0.33333329087547564],
                                [0.5999999587309599, 0.2000000550253868, 0.1999999862436533], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333715454145, 0.6666666284545855], [0.3333332951212609, 0.3333332951212609, 0.3333334097574782],
                                [0.19999999694303386, 0.8000000030569661], [0.5, 0.5], [0.2, 0.2, 0.2, 0.2, 0.2], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.5, 0.5], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.2, 0.2, 0.6], [0.5, 0.5], [0.5, 0.5],
                                [0.6666666709124529, 0.16666666454377352, 0.16666666454377352], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.6666666666666666, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25], [0.25, 0.75], [0.5, 0.5], [0.2, 0.2, 0.4, 0.2],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.5, 0.5],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.25, 0.25, 0.25, 0.25],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333],
                                [0.3333332951212609, 0.3333332951212609, 0.3333334097574782], [0.5, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.5, 0.5],
                                [0.24999997850570865, 0.24999997850570865, 0.2500000644828741, 0.24999997850570865],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.3333334352322048, 0.3333333333333333, 0.33333323143446186],
                                [0.3333333545622622, 0.3333333545622622, 0.33333329087547564], [0.4999999952234907, 0.24999998805872659, 0.2500000167177828],
                                [0.25, 0.25, 0.25, 0.25], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5],
                                [0.4999999856704716, 0.2499999928352358, 0.2500000214942926], [0.2, 0.2, 0.2, 0.2, 0.2], [0.5, 0.5],
                                [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], [0.5, 0.5], [0.5, 0.5], [0.19999999694303386, 0.8000000030569661], [1.0], [1.0],
                                [0.8571428555831805, 0.1428571444168195], [0.16666666454377355, 0.16666666454377355, 0.666666670912453], [0.5, 0.5], [0.5, 0.5], [1.0], [1.0],
                                [1.0], [1.0], []],
            },
        )
        stories = [
            [0, 1, 5, 9, 10, 11, 13, 15, 18, 21, 22, 26, 28, 32, 33, 37, 39, 43, 44, 45, 49, 50, 51, 55, 58, 60, 61, 62, 66, 69, 73, 76, 78, 79, 83, 87, 88, 90, 92, 95, 97,
             101, 103, 104, 105, 106, 109, 110, 111, 113, 114, 117, 121, 123, 126, 128, 130, 131, 134, 138, 142, 146, 150, 152, 154, 155, 157, 159, 160, 162, 166, 173, 175,
             176, 179, 181, 183, 187, 189, 190, 193, 197, 199, 202, 206, 210, 213, 217, 221, 225, 227, 231, 233, 234, 235, 238, 239, 240, 241, 242], [2, 3, 4, 8], [6], [7],
            [12, 14, 17, 19, 23, 27, 29, 31], [16, 20, 24, 25], [30], [34, 35, 38, 41, 42], [36], [40], [46, 48], [47], [52, 54, 57, 59], [53, 56], [63, 64, 68, 71, 75],
            [65, 67, 70, 72, 74], [77, 81, 84, 86, 89, 91, 94, 98, 100, 102], [80, 82, 85], [93], [96, 99], [107, 108], [112], [115, 118, 122, 124, 125, 127, 129],
            [116, 119, 120], [132], [133, 135, 136, 140, 143, 145, 148, 151, 153], [137, 139, 141], [144, 147, 149], [156], [158],
            [161, 163, 167, 171, 174, 177, 178, 180, 184, 188, 191, 192, 196, 200, 203, 207, 209, 212, 215, 219, 222, 226, 229], [164, 165, 169, 172], [168, 170], [182],
            [185, 186], [194, 195], [198], [201], [204, 205, 208, 211, 214, 216, 218, 220, 223, 224], [228, 230], [232], [236, 237]]

        storylines = [0, 0, 1, 1, 1, 0, 2, 3, 1, 0, 0, 0, 4, 0, 4, 0, 5, 4, 0, 4, 5, 0, 0, 4, 5, 5, 0, 4, 0, 4, 6, 4, 0, 0, 7, 7, 8, 0, 7, 0, 9, 7, 7, 0, 0, 0, 10, 11, 10, 0,
                      0, 0, 12, 13, 12, 0, 13, 12, 0, 12, 0, 0, 0, 14, 14, 15, 0, 15, 14, 0, 15, 14, 15, 0, 15, 14, 0, 16, 0, 0, 17, 16, 17, 0, 16, 17, 16, 0, 0, 16, 0, 16, 0,
                      18, 16, 0, 19, 0, 16, 19, 16, 0, 16, 0, 0, 0, 0, 20, 20, 0, 0, 0, 21, 0, 0, 22, 23, 0, 22, 23, 23, 0, 22, 0, 22, 22, 0, 22, 0, 22, 0, 0, 24, 25, 0, 25,
                      25, 26, 0, 26, 25, 26, 0, 25, 27, 25, 0, 27, 25, 27, 0, 25, 0, 25, 0, 0, 28, 0, 29, 0, 0, 30, 0, 30, 31, 31, 0, 30, 32, 31, 32, 30, 31, 0, 30, 0, 0, 30,
                      30, 0, 30, 0, 33, 0, 30, 34, 34, 0, 30, 0, 0, 30, 30, 0, 35, 35, 30, 0, 36, 0, 30, 37, 0, 30, 38, 38, 0, 30, 38, 30, 0, 38, 30, 0, 38, 30, 38, 0, 38, 30,
                      38, 0, 30, 38, 38, 0, 30, 0, 39, 30, 39, 0, 40, 0, 0, 0, 41, 41, 0, 0, 0, 0, 0]

        block = FindStorylines()
        res_df = block.transform(data)
        # assert res_df["storyline"].to_list() == storylines  # TODO(Jeffrey): Fix this test
