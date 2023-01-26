# Bilkent Quota Tracker

This is a tool for Bilkent University students to track the remaining quotas for their courses on the university's online registration system. It supports adding non-existing courses or non-existing sections of existing courses. It will alert the user if the section or the course does not exist, and for optimization it will not check those sections and/or courses for that run.

## Installation

1. Clone the repository: `git clone https://github.com/tolgaozgun/BilkentQuotaTracker.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Fill out the `config.json` file with your desired courses and sections. An example is provided in the repository.

## Usage

1. Run the script: `python main.py`
2. Your remaining quotas for the specified courses and sections will be displayed on the command line
3. If available, an audio alert will also be played with the frequency and duration specified in the config file
4. There is an optional `"delay"` field in the config file that is in milliseconds and it indicates the time delay between each URL request. It is not advised to make it any lower than 1000, which may result in getting blocked from Bilkent network.


## Note

- This script is only for Bilkent University students and will only work on the university's network.
- Use of this script for any illegal or unauthorized purposes is strictly prohibited.
- The developer of this script is not responsible for any misuse or consequences of use.
- The voice feature is only available for Windows users.

## Contribution

If you have any feature requests or encounter any bugs, please open an issue on the repository. Pull requests are also welcome.

## License

This project is licensed under the Creative Commons License. See the [LICENSE](LICENSE) file for details.
