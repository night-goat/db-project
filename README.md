응급실 병상 조회 웹 응용

이 프로젝트는 공공데이터 포털의 응급의료 Open API를 활용하여
지역별 병원의 응급실 및 입원 병상 현황을 조회할 수 있는 웹 응용 프로그램이다.

사용자는 시/도와 시/군/구를 선택하여 해당 지역의 병원 목록과
각 병원의 잔여 병상 수를 확인할 수 있다.
또한 전체 병원 중 잔여 응급실 병상이 많은 TOP 5 병원과
지역별 총 응급실 병상 수 통계도 함께 제공한다.

사용 기술
	•	Backend: Python, Flask
	•	Database: SQLite
	•	Frontend: HTML, CSS
	•	Data Source: 국립중앙의료원 응급의료기관 Open API

실행 방법
	1.	schema.sql을 실행하여 데이터베이스 생성
	2.	app.py 실행
	3.	브라우저에서 http://localhost:5000 접속
