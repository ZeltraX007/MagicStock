import { useState } from "react";

const ContactPage = () => {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // You can connect this to a backend or email service like Formspree
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 px-6 py-12 flex flex-col items-center">
      <div className="w-full max-w-2xl">
        <h1 className="text-4xl font-bold mb-6 text-center">Contact Us</h1>
        <p className="text-lg text-center mb-10">
          Have questions, feedback, or collaboration ideas? We'd love to hear from you.
        </p>

        {submitted ? (
          <div className="text-center text-green-600 text-xl font-medium">
            ✅ Thank you for reaching out! We’ll get back to you soon.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="name" className="block mb-1 font-semibold">
                Name
              </label>
              <input
                type="text"
                name="name"
                required
                value={form.name}
                onChange={handleChange}
                className="w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 dark:border-gray-700"
              />
            </div>

            <div>
              <label htmlFor="email" className="block mb-1 font-semibold">
                Email
              </label>
              <input
                type="email"
                name="email"
                required
                value={form.email}
                onChange={handleChange}
                className="w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 dark:border-gray-700"
              />
            </div>

            <div>
              <label htmlFor="message" className="block mb-1 font-semibold">
                Message
              </label>
              <textarea
                name="message"
                rows={6}
                required
                value={form.message}
                onChange={handleChange}
                className="w-full p-3 border rounded-md bg-gray-100 dark:bg-gray-800 dark:border-gray-700"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-black dark:bg-white text-white dark:text-black py-3 rounded hover:opacity-90 transition"
            >
              Send Message
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ContactPage;
