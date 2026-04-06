# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.


### Với 0.0
gpt4o_latency: 3.4287238121032715
mini_latency: 2.5331954956054688
gpt4o_cost_estimate: 0.00052

### Với 0.5
gpt4o_latency: 2.5094337463378906
mini_latency: 2.373570680618286
gpt4o_cost_estimate: 0.00048

### Với 1.0
gpt4o_latency: 2.064176082611084
mini_latency: 3.0107879638671875
gpt4o_cost_estimate: 0.0006133333333333334

### Với 1.5
gpt4o_latency: 2.130354642868042
mini_latency: 2.0277395248413086
gpt4o_cost_estimate: 0.0005866666666666667



## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> "Khi Temperature tăng từ 0.0 lên 1.5, nội dung phản hồi chuyển dần từ sự nhất quán, ngắn gọn sang sáng tạo và ngẫu nhiên hơn. Ở mức 1.0, câu trả lời vẫn giữ được sự mạch lạc nhưng giàu tính biểu cảm; tuy nhiên ở mức 1.5, Model bắt đầu có dấu hiệu "loạn ngôn", sử dụng từ ngữ kỳ lạ hoặc cấu trúc câu không còn chuẩn xác. Độ trễ (latency) không giảm mà thường có xu hướng tăng nhẹ khi Temperature cao do Model tạo ra nhiều từ ngữ dài dòng hơn. "

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> **ôi sẽ đặt Temperature từ 0.0 đến 0.2. Trong hỗ trợ khách hàng, sự chính xác, nhất quán và đáng tin cậy là ưu tiên hàng đầu. Mức Temperature thấp giúp chatbot bám sát kịch bản, tránh việc tự ý sáng tạo thông tin sai lệch (hallucination) và đảm bảo mọi khách hàng đều nhận được cùng một câu trả lời chuẩn xác cho cùng một vấn đề.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> *Dựa trên đơn giá 0.010 cho GPT-4o và 0.0006 cho GPT-4o-mini, GPT-4o đắt hơn khoảng 16.7 lần.

    Tổng số token mỗi ngày: 10,000 người × 3 lần × 350 tokens = 10.5 triệu tokens.

    Chi phí GPT-4o: ≈105 USD/ngày.

    Chi phí GPT-4o-mini: ≈6.3 USD/ngày.*

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> *GPT-4o xứng đáng khi: Cần giải quyết các bài toán tư duy logic phức tạp, viết code phần mềm hoặc phân tích các tài liệu pháp lý/kỹ thuật chuyên sâu nơi mà một lỗi nhỏ cũng có thể gây hậu quả lớn.

GPT-4o-mini tốt hơn khi: Thực hiện các tác vụ xử lý ngôn ngữ phổ thông với quy mô lớn (high volume) như: phân loại email rác, tóm tắt ý chính của tin nhắn, hoặc đóng vai trò là một chatbot trả lời các câu hỏi thường gặp (FAQs) đơn giản để tối ưu chi phí vận hành.*

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming quan trọng nhất khi xây dựng Chatbot tương tác trực tiếp, giúp hiển thị phản hồi ngay lập tức để giảm "thời gian chờ đợi cảm nhận" của người dùng. Ngược lại, non-streaming phù hợp hơn cho các tác vụ xử lý dữ liệu ngầm (backend) như tóm tắt văn bản hàng loạt, trích xuất dữ liệu JSON hoặc phân loại email, nơi hệ thống cần kết quả hoàn chỉnh để thực hiện các bước logic tiếp theo.*


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
