import re

lines = list(map(lambda x: x.strip(), open("4.txt", "r").readlines()))

passport_fields = []
passports = []
for line in lines:
    if not line:
        passports.append({k: v for k, v in passport_fields})
        passport_fields = []
    else:
        passport_fields.extend([tuple(kv.split(":")) for kv in line.split()])
if passport_fields:
    passports.append({k: v for k, v in passport_fields})


def is_valid_1(passport):
    return all(k in passport for k in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"))


def num_value_between(txt, min_value, max_value):
    try:
        val = int(txt)
        return min_value <= val <= max_value
    except:
        return False


hcl_p = re.compile(r"^#[0-9a-f]{6}$")
pid_p = re.compile(r"^[0-9]{9}$")


def is_valid_2(passport):
    if not num_value_between(passport.get("byr", ""), 1920, 2002):
        return False
    if not num_value_between(passport.get("iyr", ""), 2010, 2020):
        return False
    if not num_value_between(passport.get("eyr", ""), 2020, 2030):
        return False
    hgt = passport.get("hgt", "")
    if hgt.endswith("cm"):
        if not num_value_between(hgt[:-2], 150, 193):
            return False
    elif hgt.endswith("in"):
        if not num_value_between(hgt[:-2], 59, 76):
            return False
    else:
        return False
    if not hcl_p.match(passport.get("hcl", "")):
        return False
    if passport.get("ecl", "") not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        return False
    if not pid_p.match(passport.get("pid", "")):
        return False
    return True


# part 1
print(len(list(filter(is_valid_1, passports))))

# part 2
print(len(list(filter(is_valid_2, passports))))
