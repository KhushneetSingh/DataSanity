import '../styles/globals.css';
import Layout from '../components/Layout';

export default function MyApp({ Component, pageProps }) {
  // Allow each page to optionally set a `title` via getLayout or a static property
  const pageTitle = Component.pageTitle || 'Dashboard';

  return (
    <Layout title={pageTitle}>
      <Component {...pageProps} />
    </Layout>
  );
}
