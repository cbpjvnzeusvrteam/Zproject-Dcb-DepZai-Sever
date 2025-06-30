<?php
// Giao diện admin ZProject - version nâng cấp

// === Prompt ===
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["new_prompt"])) {
    file_put_contents("prompt.json", json_encode([
        "prompt" => trim($_POST["new_prompt"])
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    $status = "✅ Đã cập nhật prompt!";
}

$current_prompt = "(Chưa có prompt)";
if (file_exists("prompt.json")) {
    $json = json_decode(file_get_contents("prompt.json"), true);
    $current_prompt = $json["prompt"] ?? $current_prompt;
}

// === File người dùng ===
$user_files = glob("data_*.json");
$total_users = count($user_files);

// === File nhóm ===
$groups = [];
if (file_exists("groups.json")) {
    $groups = json_decode(file_get_contents("groups.json"), true) ?? [];
}
$total_groups = count($groups);

// === Thống kê khác ===
$total_files = count(glob("*.json"));
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>ZProject Admin</title>
    <style>
        body {
            background: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif;
            padding: 40px;
        }
        h1 { font-size: 26px; margin-bottom: 20px; color: #38bdf8; }
        h2 { color: #60a5fa; margin-top: 30px; margin-bottom: 10px; }
        textarea {
            width: 100%; height: 140px;
            background: #1e293b; border: 1px solid #334155;
            color: #f8fafc; padding: 12px; border-radius: 6px;
            font-family: monospace;
        }
        button {
            background: #38bdf8; color: #0f172a;
            border: none; padding: 10px 18px;
            font-weight: bold; margin-top: 12px;
            border-radius: 6px; cursor: pointer;
        }
        .card {
            background: #1e293b;
            padding: 15px 20px;
            border: 1px solid #334155;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .status {
            background: #16a34a; padding: 8px 12px;
            border-radius: 5px; display: inline-block;
            margin-bottom: 15px;
        }
        a {
            color: #60a5fa; text-decoration: none;
            font-size: 14px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }
    </style>
</head>
<body>

<h1>🧠 Trung tâm điều khiển <b>ZProject Bot</b></h1>

<?php if (isset($status)): ?>
    <div class="status"><?= $status ?></div>
<?php endif; ?>

<div class="grid">
    <div class="card">
        <h2>📊 Thống kê nhanh</h2>
        👥 Người dùng: <b><?= $total_users ?></b><br>
        🏘️ Nhóm: <b><?= $total_groups ?></b><br>
        📁 File JSON tổng: <b><?= $total_files ?></b>
    </div>
    <div class="card">
        <h2>⏱ Gợi ý log gần đây</h2>
        <ul>
            <li>• 19:13 → /ask bởi 58190...</li>
            <li>• 18:50 → /noti gửi 12 nhóm</li>
            <li>• 18:30 → Xổ số MB gửi auto ✅</li>
        </ul>
    </div>
</div>

<h2>🧠 Prompt hệ thống</h2>
<form method="post">
    <textarea name="new_prompt"><?= htmlspecialchars($current_prompt) ?></textarea>
    <br><button>💾 Cập nhật prompt</button>
</form>

<h2>📁 Người dùng (<?= $total_users ?>)</h2>
<ul>
<?php foreach ($user_files as $file): 
    $uid = str_replace(["data_", ".json"], "", $file);
?>
    <li class="card">
        <b><?= htmlspecialchars($file) ?></b><br>
        <a href="get.php?uid=<?= $uid ?>">Xem</a> | 
        <a href="delete.php?uid=<?= $uid ?>" onclick="return confirm('Xoá người dùng <?= $uid ?>?')">Xoá</a>
    </li>
<?php endforeach; ?>
</ul>

<h2>🏘️ Nhóm đang theo dõi (<?= $total_groups ?>)</h2>
<ul>
<?php foreach ($groups as $gid): ?>
    <li class="card">📍 Group ID: <code><?= $gid ?></code></li>
<?php endforeach; ?>
</ul>

</body>
</html>