import re

import streamlit as st
from moviepy.editor import VideoFileClip
from pytube import YouTube


output_path = 'output.mp4'
output_voice_path = 'output.wav'


def is_valid_youtube_url(url):
    # YouTube URL을 확인하기 위한 정규 표현식 패턴
    youtube_url_pattern = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube\.com/watch\?v=|youtu\.be/)'
        '[A-Za-z0-9_-]{11}'
    )
    
    return bool(youtube_url_pattern.match(url))


def download_youtube_video(url, output_path):
    if not is_valid_youtube_url(url):
        raise ValueError('유효한 YouTube URL이 아닙니다.')
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download(filename=output_path)



def voice_extraction(video_path, start_time, end_time, output_voice_path):
    
    # 비디오 파일 로드
    video = VideoFileClip(video_path)
    # 지정된 시간 동안의 오디오 추출
    audio_clip = video.subclip(start_time, end_time).audio
    # WAV 파일로 저장
    audio_clip.write_audiofile(output_voice_path)
    


st.write("## 유튜브 영상에서 음성 추출하기")


video_path = st.text_input(
        "Enter YouTube URL 👇",
        # label_visibility=st.session_state.visibility,
        # disabled=st.session_state.disabled,
        # placeholder=st.session_state.placeholder,
    )

start_time = st.number_input(step=1, label='Insert a start time')
st.write('The start time is ', start_time)

end_time = st.number_input(step=1, label='Insert a end time')
st.write('The end time is ', end_time)



if st.button('시작'):
    if start_time >= end_time:
        st.error('시작 시간은 종료 시간보다 작아야 합니다.')
        st.stop()
        
    print(f"video_path - {video_path}")
    print(f"start_time - {start_time}")
    print(f"end_time - {end_time}")

    with st.spinner('잠시만 기다려주세요...'):
        
        download_youtube_video(video_path, output_path)
        voice_extraction(output_path, start_time, end_time, output_voice_path)
        with open(output_voice_path, "rb") as file:    
            btn = st.download_button(
                    label="Download wav file",
                    data=file,
                    file_name=output_voice_path,
                    mime="audio/wav"
                )


# def main():
#     video_path = 'https://www.youtube.com/watch?v=Jk7hYAwhkT8'
#     start_time = 10
#     end_time = 20
#     download_youtube_video(video_path, output_path)
#     print(f"File download successe : {output_path}")
    
#     voice_extraction(output_path, start_time, end_time, output_wave_path)
#     print(f"Voice extraction complete : {output_wave_path}")

# if __name__ == '__main__':
#     main()
#     print(f"end main")

