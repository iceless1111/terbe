import re, os, pathlib, sys, types
from importlib import util as importlib_util

def Base(org, orgfull="0123456789", newfull="0123456789abcdef"):
    def _tostr(n, e):
        base = len(e)
        if n < base:
            return e[n]
        else:
            return _tostr(n//base, e) + e[n%base]

    #be ten base
    tenbase = 0
    tmp1 = 0
    for tmp in org:
        tenbase += orgfull.index(tmp) * pow(len(orgfull), (len(org) - 1 - tmp1))
        tmp1 += 1
    
    #be newfull
    return _tostr(tenbase, newfull)

def Count(main_str, target, skip=[]):
    for (start, end) in skip:
        for tmp in Regex(main_str, start, end):
            main_str = main_str.replace(f"{start}{tmp}{end}", "", 1)
    
    result = 0
    while main_str != "":
        if main_str.startswith(target):
            main_str = main_str.replace(target, "", 1)
            result += 1
        else:
            main_str = main_str[1:]
    
    return result

def Split(s, delimiter=' ', skip=None, retain=False):
    if skip is None:
        skip = []

    tokens = []
    current_token = []
    i = 0
    length = len(s)
    delimiter_length = len(delimiter)
    
    while i < length:
        # Check for skip markers
        skip_found = False
        for skip_start, skip_end in skip:
            if s[i:i+len(skip_start)] == skip_start:
                skip_found = True
                if retain:
                    # Include the skip_start marker if retain is True
                    current_token.append(skip_start)
                # Skip over the skip_start marker
                i += len(skip_start)
                while i < length and s[i:i+len(skip_end)] != skip_end:
                    current_token.append(s[i])
                    i += 1
                if i < length:
                    # Skip over the skip_end marker
                    if retain:
                        # Include the skip_end marker if retain is True
                        current_token.append(skip_end)
                    i += len(skip_end)
                break
        
        if skip_found:
            continue
        
        # Check if we hit the delimiter
        if s[i:i+delimiter_length] == delimiter:
            if current_token:
                tokens.append(''.join(current_token).strip())
                current_token = []
            # If we're at the end of the string, add an empty token if needed
            if i + delimiter_length == length:
                tokens.append('')
            i += delimiter_length
        else:
            # Collect the current character into the token
            current_token.append(s[i])
            i += 1

    # Add the last token if there's any
    if current_token:
        tokens.append(''.join(current_token).strip())

    return tokens

def ReplaceFromLast(string, old, new, time=None):
    if time is None:
        return string.replace(old, new)
    else:
        return new.join(string.rsplit(old, time))

def Replace(original, replace, skip):
    skip_patterns = '|'.join([rf'{re.escape(start)}.*?{re.escape(end)}' for start, end in skip])
    
    combined_pattern = rf'({skip_patterns})|([^{skip_patterns}]+)'

    def replace_match(match):
        if match.group(1) is not None:
            return match.group(1)
        
        segment = match.group(2)
        for key, value in replace.items():
            segment = segment.replace(key, value)
        return segment
    
    result = re.sub(combined_pattern, replace_match, original, flags=re.DOTALL)
    
    return result

def Regex(string: str, start: str, end: str, skip: list=None):
    def _parseContent(s, start_marker, end_marker, skip):
        if skip is None:
            skip = []
        
        results = []
        i = 0
        while i < len(s):
            # Check for skip markers
            skip_found = False
            for skip_start, skip_end in skip:
                if s[i:i+len(skip_start)] == skip_start:
                    skip_found = True
                    # Skip until we find the corresponding end marker
                    i += len(skip_start)
                    while i < len(s) and s[i:i+len(skip_end)] != skip_end:
                        i += 1
                    if i < len(s):
                        i += len(skip_end)
                    break
            if skip_found:
                continue
            
            if s[i:i+len(start_marker)] == start_marker:
                i += len(start_marker)
                start = i
                while i < len(s) and s[i:i+len(end_marker)] != end_marker:
                    i += 1
                if i < len(s):
                    results.append(s[start:i])
                    i += len(end_marker)
            else:
                i += 1
        
        return results
    
    return _parseContent(string, start, end, skip)

def dictOverWrite(FROM, TO):
    result = TO.copy()
    result.update(FROM)
    return result

import os
import pathlib
import importlib.util
import sys

def Import(path, full=False, tmpname=None):
    if os.path.isdir(path):
        tmptype = "dir"
    elif os.path.isfile(path):
        tmptype = "file"
    else:
        raise FileNotFoundError(path)
    if not tmpname:
        if tmptype == "file":
            tmpname = pathlib.Path(path).stem
        if tmptype == "dir":
            tmpname = pathlib.Path(path).name
    if full:
        tmppath = path
    else:
        if tmptype == "file":
            tmppath = path
        if tmptype == "dir":
            tmppath = os.path.join(path, "__init__.py")
    if tmpname == "__main__" and tmptype == "dir" and os.path.isfile(os.path.join(path, "__main__.py")):
        tmppath = os.path.join(path, "__main__.py")
    tmp = importlib.util.spec_from_file_location(tmpname, tmppath)
    run = importlib.util.module_from_spec(tmp)
    tmp.loader.exec_module(run)
    if tmpname == "__main__" and tmptype == "dir" and os.path.isfile(os.path.join(path, "__main__.py")) and "__main__" in run.__dict__ and callable(run.__dict__["__main__"]):
        run.__dict__["__main__"]()
    return run

def ImportFromString(string, name="__main__"):
    namespace = types.ModuleType(name)
    exec(string, namespace.__dict__)
    return namespace

class _ExitBlocked(Exception): pass

class _NoExit:
    def __enter__(self):
        self.original_exit = sys.exit
        sys.exit = self._no_exit

    def _no_exit(self, code=0):
        raise _ExitBlocked(code)

    def __exit__(self, exc_type, exc_value, traceback):
        sys.exit = self.original_exit

def DoWithoutExit(target):
    exit_code = 0
    try:
        with _NoExit():
            target()
    except _ExitBlocked as e:
        exit_code = e.args[0]
    return exit_code

def SandBox(argv):
    oldSysArgv = sys.argv
    sys.argv = argv
    exitCode = DoWithoutExit(lambda: Import(argv[0], tmpname="__main__"))
    sys.argv = oldSysArgv
    return exitCode