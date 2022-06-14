from google_api import get_video_by_location, is_necessary_period

if __name__ == '__main__':
    latitude = 52.311546
    longitude = 4.760798
    radius_km = 1
    data_from = '2012-01-01'
    data_to = '2012-12-31'

    videos_id = get_video_by_location(latitude, longitude, radius_km)
    videos_id = list(filter(lambda video_id: is_necessary_period(videos_id, data_from=data_from, data_to=data_to),
                            videos_id))
    print(f'C {data_from} по {data_to} на YouTube было загружено {len(videos_id)} видео из области '
          f'радиусом {radius_km}км вокруг ({latitude}, {longitude}).')
