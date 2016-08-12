import json
import subprocess
from elks.helpers import (
    elksapi,
    parser_inject_generics,
    elks_store_media
)

from elks.formatting import (
    bytes_to_human,
    duration_to_human,
    kv_print
)

descr = """\
Handle phone call recordings"""

def main(args):
    if args.recording_id:
        response = [elksapi(args, 'recordings/%s' % args.recording_id)]
        if args.open:
            wav_src = 'recordings/%s.wav' % args.recording_id
            filedest = '/tmp/elks-%s.wav' % args.recording_id
            pretty_print_recording(response[0], pretty = args.pretty)
            elks_store_media(args, wav_src, filedest)

            print('[Playing...]')
            # TODO Cross-platform and fix macOS playback
            subprocess.call(['afplay', filedest])
            print('[Played]')
            print('Recording stored in %s' % filedest)
            return
    else:
        response = elksapi(args, 'recordings')['data']
        if args.open:
            print('Cannot play multiple recordings. Please set recording_id')
            exit(1)
    for recording in response:
        pretty_print_recording(recording, pretty = args.pretty)
        if args.verbose:
            call_res = elksapi(args, 'calls/%s' % recording['callid'])
            kv_print('From:', call_res['from'])
            kv_print('To:', call_res['to'])
            kv_print('Actions:', json.dumps(call_res['actions']))

def parse_arguments(parser):
    parser.description = descr
    parser.add_argument('-p', '--pretty', action='store_true',
            help='Print human friendly numbers')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Print detailed information')
    parser.add_argument('recording_id', nargs='?',
            help='Select a specific recording')
    parser.add_argument('--open', action='store_true',
            help='Try to play the selected recording')
    parser_inject_generics(parser)

def pretty_print_recording(recording, pretty = False):
    if pretty:
        size = bytes_to_human(recording.get('bytes', 0))
    else:
        size = recording.get('bytes', 0)

    if pretty:
        duration = duration_to_human(recording.get('duration', 0))
    else:
        duration = recording.get('duration', 0)

    print('%s %s %s %s' % (
        recording['created'],
        recording['id'],
        duration,
        size
    ))

