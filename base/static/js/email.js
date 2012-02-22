// This script is (c) copyright 2008 by Dan Appleman under the
// GNU General Public License (http://www.gnu.org/licenses/gpl.html)
// This script is modified from an original script by Jim Tucek
// For more information, visit www.danappleman.com
// Leave the above comments alone!
// see encryption_instructions.txt for explanation of usage

var decryption_cache = [];

var addresses = [
    "10873 10867 4088 2761 4719 493 4520 7189 10795 5957 6930 4719 493 4719 5957 5957 3541 9373 7189 493 493 8439 5252 4088 2761 9423 9423 2648 10244 4088 2761 4719 493 3541 4237 7189 4088"
];

// Finds base^exponent % y for large values of (base^exponent)
function exponentialModulo(base, exponent, y) {
    var answer;
    var temp;
    var i;

    if (y % 2 === 0) {
        answer = 1;

        for(i = 1; i <= y/2; i += 1) {
            temp = (base * base) % exponent;
            answer = (temp * answer) % exponent;
        }
    } else {
        answer = base;

        for(i = 1; i <= y/2; i += 1) {
            temp = (base * base) % exponent;
            answer = (temp * answer) % exponent;
        }
    }

    return answer;
}

function decrypt_string(crypted_string, n, decryption_key, just_email_address) {
    var cache_index = "'" + crypted_string + "," + just_email_address + "'";

    if(decryption_cache[cache_index]) {
        return decryption_cache[cache_index];
    }

    if(addresses[crypted_string]) {
        crypted_string = addresses[crypted_string];
    }

    if(!crypted_string.length) {
        return "Error, not a valid index.";
    }

    if(n === 0 || decryption_key === 0) {
        var numbers = crypted_string.split(' ');
        n = numbers[0]; decryption_key = numbers[1];
        numbers[0] = ""; numbers[1] = "";
        crypted_string = numbers.join(" ").substr(2);
    }

    var decrypted_string = '';
    var crypted_characters = crypted_string.split(' ');

    for(var key in crypted_characters) {
        if (crypted_characters.hasOwnProperty(key)) {
            var current_character = crypted_characters[key];
            var decrypted_character = exponentialModulo(current_character,n,decryption_key);

            if(just_email_address && key < 7) {
                continue;
            }

            if(just_email_address && decrypted_character === 63) {
                break;
            }

            decrypted_string += String.fromCharCode(decrypted_character);
        }
    }

    decryption_cache[cache_index] = decrypted_string;

    return decrypted_string;
}

function decrypt_and_email(crypted_string,n,decryption_key) {
    if(!n || !decryption_key) {
        n = 0;
        decryption_key = 0;
    }

    if(!crypted_string) {
        crypted_string = 0;
    }

    var decrypted_string = decrypt_string(crypted_string,n,decryption_key,false);
    parent.location = decrypted_string;
}

function decrypt_and_echo(crypted_string,n,decryption_key) {
    if(!n || !decryption_key) {
        n = 0;
        decryption_key = 0;
    }
    if(!crypted_string) {
        crypted_string = 0;
    }

    var decrypted_string = decrypt_string(crypted_string,n,decryption_key,true);
    document.write(decrypted_string);
    return true;
}
