#!/usr/bin/env python3

# Copyright (c) 2021 Mobvoi Inc. (authors: Binbin Zhang)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('wav_file', help='wav file')
    parser.add_argument('text_file', help='text file')
    parser.add_argument('duration_file', help='duration file')
    parser.add_argument('output_file', help='output list file')   # TODO：根据传label文件和txt文件来确定数据格式，这样其他的run.sh都要变
    args = parser.parse_args()

    wav_table = {}
    with open(args.wav_file, 'r', encoding='utf8') as fin:
        for line in fin:
            arr = line.strip().split()
            assert len(arr) == 2
            wav_table[arr[0]] = arr[1]

    duration_table = {}
    with open(args.duration_file, 'r', encoding='utf8') as fin:
        for line in fin:
            arr = line.strip().split()
            assert len(arr) == 2
            duration_table[arr[0]] = float(arr[1])

    with open(args.text_file, 'r', encoding='utf8') as fin, \
         open(args.output_file, 'w', encoding='utf8') as fout:
        for line in fin:
            arr = line.strip().split(maxsplit=1)
            key = arr[0]
            if arr[1].isdigit():
                label = int(arr[1])
                txt = None
            else:
                label = -1
                txt = arr[1]
            assert key in wav_table
            wav = wav_table[key]
            assert key in duration_table
            duration = duration_table[key]
            line = dict(key=key, label=label, duration=duration, wav=wav)
            if txt is not None:
                line.update({'txt': txt})
            json_line = json.dumps(line, ensure_ascii=False)
            fout.write(json_line + '\n')

