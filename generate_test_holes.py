import generate_hole


code = generate_hole.generate(radius=0.45, center_x=0, center_y=0, tool_width=0.8, depth=2.0, feed_depth=0.2, ver_feed_rate=100, holi_feed_rate=300, feed_deg=3)
print(code)

