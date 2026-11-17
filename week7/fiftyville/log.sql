-- Fiftyville investigation log
-- Theft on July 28, 2025, on Humphrey Street. The CS50 Duck was stolen at 10:15am at the bakery.
-- Read the crime scene report for July 28, 2025, on Humphrey Street to learn what happened and when.
SELECT * FROM crime_scene_reports WHERE year = 2025 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
-- The report says the theft was at 10:15am at the bakery and three witnesses were interviewed.
-- Read the interviews from July 28, 2025, to get clues from the witnesses.
SELECT name, transcript FROM interviews WHERE year = 2025 AND month = 7 AND day = 28;
-- Ruth saw the thief leave the bakery parking lot within ten minutes of the 10:15am theft.
-- List cars that exited the bakery parking lot between 10:15am and 10:25am on July 28, 2025.
SELECT license_plate FROM bakery_security_logs WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit';
-- Eight plates exited: 5P2BI95, 94KL13X, 6P58WS2, 4328GD8, G412CB7, L93JTIZ, 322W7JE, 0NTHK55.
-- Eugene saw the thief withdrawing money at the ATM on Leggett Street that morning.
-- List withdrawals at the Leggett Street ATM on July 28, 2025.
SELECT account_number, amount FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
-- Find the people who own those bank accounts.
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE bank_accounts.account_number IN (28500762, 28296815, 76054385, 49610011, 16153065, 25506511, 81061156, 26013199);
-- ATM withdrawers were Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, and Benista.
-- Raymond said the thief called someone for less than a minute while leaving the bakery.
-- List phone calls on July 28, 2025, lasting less than 60 seconds.
SELECT caller, receiver FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 60;
-- Find people who both made a short call that day and own a car that exited the bakery at 10:15-10:25am.
SELECT name, phone_number, license_plate FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 60) AND license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55');
-- That gives Sofia, Diana, Kelsey, and Bruce. Only Bruce and Diana are also among the ATM withdrawers.
-- Raymond also said the thief planned to take the earliest flight out of Fiftyville tomorrow, July 29, 2025.
-- Find the earliest flight out of Fiftyville on July 29, 2025.
SELECT id, origin_airport_id, destination_airport_id, hour, minute FROM flights WHERE year = 2025 AND month = 7 AND day = 29 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute LIMIT 5;
-- The earliest flight is flight 36 at 8:20am, to airport 4. Find that airport city.
SELECT city, full_name FROM airports WHERE id = 4;
-- Airport 4 is LaGuardia Airport in New York City, so the thief escaped to New York City.
-- List the passengers on flight 36 to see which suspect was on it.
SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number WHERE passengers.flight_id = 36;
-- Bruce was on flight 36, Diana was not. So the thief is Bruce.
-- The accomplice is the person Bruce called for less than a minute on July 28, 2025.
-- Find the calls Bruce made that day.
SELECT caller, receiver, duration FROM phone_calls WHERE caller = '(367) 555-5533' AND year = 2025 AND month = 7 AND day = 28;
-- Bruce called (375) 555-8161 for 45 seconds. Find who owns that number.
SELECT name FROM people WHERE phone_number = '(375) 555-8161';
-- That number belongs to Robin, so the accomplice is Robin.
-- CONCLUSION: The thief is Bruce. He escaped to New York City. The accomplice is Robin.
-- Bruce withdrew money at Leggett Street, left the bakery at 10:15-10:25am in car 94KL13X, called Robin for 45 seconds, and took flight 36 at 8:20am on July 29, 2025, to New York City.
