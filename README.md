# currency-monitor
Monitor my favorite currencies with an analog touch
![image](https://github.com/mlucchelli/currency-monitor/assets/17179003/61aa7f5d-5946-44c0-80f2-6999a9f714e6)

# Currency Monitor for Raspberry Pi Pico

![Currency Monitor](app_screenshot.png)

Monitor the values of your favorite currencies and cryptocurrencies with an analog touch. This MicroPython-based application allows you to view real-time and historical data for various currencies and assets.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [Latest Exchange Rates](#latest-exchange-rates)
  - [Historical Data](#historical-data)
- [Tools](#tools)
- [Contributing](#contributing)
- [Reading Material](#reading-material)

## Getting Started

1. **Setting Up Raspberry Pi Pico:** Ensure your Raspberry Pi Pico is properly set up and running MicroPython.
2. **Wiring:** Connect the display and [Pomoroni RGB potentiometer](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-rgb-potentiometer) to your Raspberry Pi Pico following the wiring diagram provided in the documentation.
3. **Installing Dependencies:** Make sure you have the required MicroPython libraries installed for display and internet connectivity. Refer to the documentation for details.
4. **Running the Application:** Upload the application code to your Raspberry Pi Pico and run it.
5. **Interact with the Potentiometer:** Use the RGB potentiometer to navigate the user interface, changing colors according to the selected currency (Work in Progress).
6. **View Currency Data:** Monitor the values of various currencies and assets in real time.

## Wiring

![Untitled](https://github.com/mlucchelli/currency-monitor/assets/17179003/dfaf2ceb-cd28-4041-b6c0-6c4bc6cd76e7)

## Installation



## Usage


## API Endpoints

### Latest Exchange Rates

- **Endpoint:** `/latest`
- **Description:** Get the latest exchange rates for a set of currencies and cryptocurrencies.

### Historical Data

- **Endpoint:** `/historic/:days`
- **Description:** Retrieve historical data for a specified number of days.

## Tools



## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them.
Create a pull request with a clear description of your changes.
## Reading Material

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the MicroPython community for their support and contributions.
- Inspired by the need for a simple and interactive currency monitoring solution.
