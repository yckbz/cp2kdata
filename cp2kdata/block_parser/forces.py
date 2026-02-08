import regex as re
import numpy as np

ATOMIC_FORCES_RE_OLD = re.compile(
    r"""
    \sATOMIC\sFORCES\sin\s\[a\.u\.\]\s*\n
    \n
    \s\#.+\n
    (
        \s+(?P<atom>\d+)
        \s+(?P<kind>\d+)
        \s+(?P<element>\w+)
        \s+(?P<x>[\s-]\d+\.\d+)
        \s+(?P<y>[\s-]\d+\.\d+)
        \s+(?P<z>[\s-]\d+\.\d+)
        \n
    )+
    """,
    re.VERBOSE
)

ATOMIC_FORCES_RE_NEW = re.compile(
    r"""
    \sFORCES\|\sAtomic\sforces\s\[.+?\]\s*\n
    \sFORCES\|\s+Atom\s+x\s+y\s+z\s+\|f\|\s*\n
    (
        \sFORCES\|\s+
        (?P<atom>\d+)
        \s+(?P<x>[\d\.\-E\+]+)
        \s+(?P<y>[\d\.\-E\+]+)
        \s+(?P<z>[\d\.\-E\+]+)
        \s+[\d\.\-E\+]+
        \n
    )+
    """,
    re.VERBOSE
)


def parse_atomic_forces_list(output_file):
    atomic_forces_list = []
    
    matches = list(ATOMIC_FORCES_RE_OLD.finditer(output_file))

    if not matches:
        matches = list(ATOMIC_FORCES_RE_NEW.finditer(output_file))

    for match in matches:
        atomic_forces = []
        for x, y, z in zip(*match.captures("x", "y", "z")):
            atomic_forces.append([x, y, z])
        atomic_forces_list.append(atomic_forces)

    if atomic_forces_list:
        return np.array(atomic_forces_list, dtype=float)
    else:
        return None
