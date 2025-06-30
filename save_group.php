<?php
header('Content-Type: text/plain');

$data = json_decode(file_get_contents("php://input"), true);
if (!isset($data["group_id"])) {
    http_response_code(400);
    echo "❌ Thiếu group_id!";
    exit;
}

$gid = preg_replace("/[^0-9\-]/", "", $data["group_id"]);
if (!$gid) {
    echo "❌ ID không hợp lệ!";
    exit;
}

$group_name = trim($data["group_name"] ?? "Chưa biết");
$username = trim($data["username"] ?? "");
$now = date("Y-m-d H:i:s");

$file = "groups_db.json";
$existing = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

$found = false;
foreach ($existing as &$entry) {
    if ($entry["group_id"] == $gid) {
        $found = true;
        $entry["group_name"] = $group_name;
        $entry["username"] = $username;
        break;
    }
}
unset($entry);

if (!$found) {
    $existing[] = [
        "group_id" => $gid,
        "group_name" => $group_name,
        "username" => $username,
        "joined_at" => $now
    ];
}

file_put_contents($file, json_encode($existing, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
echo $found ? "🔄 Đã cập nhật nhóm: $gid" : "✅ Đã thêm nhóm mới: $gid";