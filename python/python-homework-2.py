import random
import statistics

class Metrics:
    def __init__(self):
        self.cpu_data = [random.randint(0, 100) for _ in range(8)]
        self.memory_used = random.randint(300, 2048)
        self.memory_total = 2048
        self.load_avg = (
            statistics.mean(self.cpu_data) * 1.0054
        )  # just to have more digits
        self.agent = "metric-gatherer.%s" % random.randint(1000, 9999)
        self.agent_address = random.choice([16384, 32768, 4096])

M = Metrics()

def format_with_fstring():
    sys_info = f"CPU #1: {M.cpu_data[1]}%, Memory used: {M.memory_used}, Load avg: {M.load_avg:.2f}"
    return f"{sys_info:*^64}"

def format_with_format():
    format_pid = M.agent 
    sys_info = "[{pid}] CPU #7: {cpu7}%, Memory used: {mused}, Load avg: {lavg:.2f}".format(
            pid = M.agent[-4:],
            cpu7 = M.cpu_data[7],
            mused = M.memory_used,
            lavg = M.load_avg
            )
    return "{:->64}".format(sys_info)

def format_with_percent():
    pid = M.agent_address
    cpu_7 = M.cpu_data
    mused = M.memory_used
    lavg = M.load_avg
    return "%*s" % (64, "[%#x] CPU #7: %i%%, Memory used: %i, Load avg: %.2f" % (M.agent_address, M.cpu_data[7], M.memory_used, M.load_avg))


#### Tests ####

import unittest
from string import Template


class TestStringFormatters(unittest.TestCase):
    def get_data(self):
        return M

    def get_pid(self, agent: str) -> str:
        acc = ""
        found_dot = False
        for char in agent:
            if found_dot:
                acc += char
            if char == ".":
                found_dot = True
        assert len(acc) == 4, acc
        return acc

    def test_fstring(self):
        data = self.get_data()
        fstring_template = Template(
            "CPU #1: $cpu_1%, Memory used: $mem_used, Load avg: $load_avg"
        )
        templated = fstring_template.substitute(
            cpu_1 = data.cpu_data[1],
            mem_used = data.memory_used,
            load_avg = f"{data.load_avg:.2f}"
        )
        formatted = templated.center(64, "*")

        user_result = format_with_fstring()
        self.assertEqual(user_result, formatted)

    def test_format_method(self):
        """
        For example:
            "[3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23"
        should become
            "------------[3124] CPU #7: 25%, Memory used: 450, Load avg: 3.23"
        """
        data = self.get_data()
        fstring_template = Template(
            "[$pid] CPU #7: $cpu_7%, Memory used: $mem_used, Load avg: $load_avg"
        )
        templated = fstring_template.substitute(
            pid = self.get_pid(data.agent),
            cpu_7 = data.cpu_data[7],
            mem_used = data.memory_used,
            load_avg = '{:.2f}'.format(data.load_avg)
        )
        formatted = templated.rjust(64, "-")

        user_result = format_with_format()
        self.assertEqual(user_result, formatted)
    
    def test_format_percent(self):
        """
        For example:
            "[0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25"
        should become
            "'          [0x4000] CPU #7: 87%, Memory used: 900, Load avg: 1.25'"
        """
        data = self.get_data()
        fstring_template = Template(
            "[$hex] CPU #7: $cpu_7%, Memory used: $mem_used, Load avg: $load_avg"
        )
        templated = fstring_template.substitute(
            hex = hex(data.agent_address),
            cpu_7 = data.cpu_data[7],
            mem_used = data.memory_used,
            load_avg = "%.2f" % (data.load_avg),
        )
        formatted = templated.rjust(64, " ")

        user_result = format_with_percent()
        self.assertEqual(user_result, formatted)


if __name__ == "__main__":
    unittest.main()
